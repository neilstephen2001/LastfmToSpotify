def remove_punctuation(name: str):
    punctuation = """{};:'",<>@#$%^&*_~"""
    for i in name:
        if i in punctuation:
            if i == '&':
                name = name.replace(i, 'and')
            elif i == '/' or i == '\\':
                name = name.replace(i, " ")
            else:
                name = name.replace(i, "")
    return name


def make_embedded_url(playlist_url: str):
    split_url = playlist_url.partition(".com/")
    embedded_url = split_url[0] + split_url[1] + 'embed/' + split_url[2] + '?utm_source=generator&theme=0'
    return embedded_url


def exceptions(response):
    print("Exception occurred with status code: ", response.status_code)
    print("Error: ", response.text)
