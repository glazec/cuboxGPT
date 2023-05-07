import requests
from bs4 import BeautifulSoup
from rich import print, pretty
from rich.progress import track
from rich.console import Console
pretty.install()
console = Console()

# @todo for failed links, try seleum to download the content
# @todo fileName too long
# @todo add parse for twitter,weixin,youtube(pase cjk error) and some websites similar title
# @todo add update mechanism
# @todo add multi-threading
# @todo get title through open media


def webLoader(links):
    # open cubox/cubox.txt file and read line by line
    # for each line, download the content and save it to a file
    errorLinks = []
    shortContentLinks = []
    for step in track(range(len(links)), description="Downloading"):
        url = links[step].strip()
        try:
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                content = soup.get_text('.')
                # title parse for figma
                if "figma" in url:
                    title = url.split('/')[-1]
                # regualr title parse. Use title in default, otherwise use domain name
                else:
                    if (soup.title is None):
                        # set title as the domain of the url
                        title = url.split('/')[2]
                    else:
                        title = soup.title.string
                        title = title
                # make sure there is a title
                if title == "":
                    title = url.split('/')[2]
                title = title.strip().replace('/', '-').replace('\n', '')
                fileName = f'text/{title}.txt' if len(
                    title) <= 130 else f'text/{title[:130]}.txt'
                with open(fileName, 'w') as f:
                    f.write(f'{title}.\n')
                    f.write(f'{url}.\n')
                    f.write(content.strip().replace("\n", ""))
                wordLength = len(content.strip().replace("\n", ""))
                if wordLength < 100:
                    shortContentLinks.append(url)
                if title == "滑块验证":
                    errorLinks.append(url)
                print(
                    f'Downloaded [bold magenta]{title}[/bold magenta]')
            else:
                errorLinks.append(url)
                print(
                    f'Error downloading content [bold red]{url}[/bold red]')
        except Exception as e:
            errorLinks.append(url)
            print(
                f'Error connecting content [bold red]${url}[/bold red]')
            print(e)
    console.print("[bold blue]====Summary====[/bold blue]")
    console.print(
        f'[bold green]Sucessfully downloaded {len(links)-len(errorLinks)} links[/bold green]')
    console.print(
        f'[bold red][Error] Failed to download the following {len(errorLinks)} links:[/bold red]')
    console.print(errorLinks)
    console.print(
        f'[bold magenta][Warning] Content less than 100 words for the following {len(shortContentLinks)} links:[/bold magenta]')
    console.print(shortContentLinks)


def cuboxExportLoader(filePath):
    with open(filePath) as f:
        soup = BeautifulSoup(f, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a')]
    return links


def loadWebContentFromCuboxExport(filepath):
    links = cuboxExportLoader(filepath)
    webLoader(links)


if __name__ == '__main__':
    loadWebContentFromCuboxExport()
