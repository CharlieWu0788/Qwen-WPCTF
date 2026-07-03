import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def normalize_login_url(url):
    parsed = urlparse(url)

    return (
        f"{parsed.scheme}://"
        f"{parsed.netloc}"
        f"{parsed.path}"
    )


def scan_auth(url):
    """
    Auth Scan v1.1.0

    Layers:
    - Link discovery
    - Form discovery
    - Endpoint probing
    - Validation engine
    - Function entry collection
    """

    LOGIN_KEYWORDS = [
        "login",
        "log in",
        "sign in",
        "signin",
        "auth",
        "account"
    ]

    COMMON_LOGIN_PATHS = [
        "/wp-login.php",
        "/login",
        "/signin",
        "/admin",
        "/user/login"
    ]

    evidence = []
    detected = False

    login_urls = set()

    # NEW
    discovered_links = []

    try:

        response = requests.get(
            url,
            timeout=20,
            allow_redirects=True
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # ----------------------------
        # Step 1: Link Discovery
        # ----------------------------
        for a_tag in soup.find_all("a"):

            href = a_tag.get("href")

            if not href:
                continue

            text = (
                a_tag.get_text(strip=True)
                or ""
            )

            full_url = urljoin(
                url,
                href
            )

            # NEW
            discovered_links.append({
                "text": text,
                "url": full_url
            })

            normalized_url = normalize_login_url(
                full_url
            )

            lower_href = href.lower()
            lower_text = text.lower()

            if any(
                keyword in lower_href
                or keyword in lower_text
                for keyword in LOGIN_KEYWORDS
            ):

                login_urls.add(
                    normalized_url
                )

                evidence.append({
                    "method": "link",
                    "detail": (
                        f"Login link detected: "
                        f"{normalized_url}"
                    ),
                    "url": normalized_url
                })

        # ----------------------------
        # Step 1.5: Endpoint Probe
        # ----------------------------
        for path in COMMON_LOGIN_PATHS:

            probe_url = urljoin(
                url,
                path
            )

            try:

                r = requests.get(
                    probe_url,
                    timeout=5,
                    allow_redirects=True
                )

                content = r.text.lower()

                if (
                    "password" in content
                    and "login" in content
                ):

                    detected = True

                    login_urls.add(
                        normalize_login_url(
                            r.url
                        )
                    )

                    evidence.append({
                        "method": "endpoint_probe",
                        "detail": (
                            f"Login endpoint "
                            f"confirmed at {r.url}"
                        ),
                        "url": r.url
                    })

            except requests.RequestException:
                continue

        # ----------------------------
        # Step 2: Form Discovery
        # ----------------------------
        for form in soup.find_all("form"):

            inputs = form.find_all(
                "input"
            )

            has_password_field = any(
                i.get(
                    "type",
                    ""
                ).lower() == "password"
                for i in inputs
            )

            if has_password_field:

                action = form.get(
                    "action",
                    ""
                )

                form_url = urljoin(
                    response.url,
                    action
                )

                login_urls.add(
                    normalize_login_url(
                        form_url
                    )
                )

                evidence.append({
                    "method": "form_discovery",
                    "detail": (
                        f"Login form detected "
                        f"at {form_url}"
                    ),
                    "url": form_url
                })

        # ----------------------------
        # Step 3: Validation
        # ----------------------------
        for login_url in list(
            login_urls
        ):

            try:

                r = requests.get(
                    login_url,
                    timeout=10,
                    allow_redirects=True
                )

                content = r.text.lower()

                if (
                    "password" in content
                    and (
                        "username" in content
                        or "login" in content
                    )
                ):

                    detected = True

                    evidence.append({
                        "method": "validation",
                        "detail": (
                            f"Login page "
                            f"confirmed at {r.url}"
                        ),
                        "url": r.url
                    })

            except requests.RequestException as e:

                evidence.append({
                    "method": "error",
                    "detail": str(e),
                    "url": login_url
                })

        # ----------------------------
        # Step 4: Fallback
        # ----------------------------
        if not login_urls:

            if "login" in response.text.lower():

                detected = True

                evidence.append({
                    "method": "fallback",
                    "detail": (
                        "Login keyword found "
                        "in homepage"
                    ),
                    "url": url
                })

        # ----------------------------
        # Cleanup
        # ----------------------------
        login_urls = [
            u
            for u in login_urls
            if any(
                x in u.lower()
                for x in [
                    "login",
                    "wp-login",
                    "signin",
                    "admin"
                ]
            )
        ]

        return {
            "login_page_found": detected,
            "login_urls": list(login_urls),

            # NEW
            "discovered_links":
                discovered_links,

            "final_url": response.url,
            "evidence": evidence,
            "error": None
        }

    except requests.RequestException as e:

        return {
            "login_page_found": False,
            "login_urls": [],

            # NEW
            "discovered_links": [],

            "final_url": [],
            "evidence": [],
            "error": str(e)
        }