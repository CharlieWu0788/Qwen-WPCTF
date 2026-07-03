import requests


def check_environment(url):

    try:

        response = requests.get(
            url,
            timeout=5,
            allow_redirects=True
        )

        return {

            "reachable": True,

            "status_code": response.status_code,

            "final_url": response.url

        }

    except Exception as e:

        return {

            "reachable": False,

            "status_code": None,

            "final_url": url,

            "error": str(e)

        }