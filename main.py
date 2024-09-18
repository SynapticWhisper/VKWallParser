import argparse
from datetime import datetime
from functools import reduce

from tools.xslx_writer import save_to_excel

def main():
    parser = argparse.ArgumentParser(description='VK Data Scraper')
    parser.add_argument('group_url', help='Ссылка на группу VK')
    parser.add_argument('start_date', help='Начало периода (YYYY-MM-DD)')
    parser.add_argument('output_file', help='Путь до файла с результатами (.xlsx)')
    args = parser.parse_args()

    owner_id = None
    domain = None

    _group: str = args.group_url.split('/')[-1]
    values = ("event", "club", "public")
    is_owner_id = any(_group.startswith(value) for value in values)
    if is_owner_id:
        owner_id = _group
        for value in values:
            owner_id = owner_id.strip(value)
    else:
        domain = _group
    start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
    save_to_excel(args.output_file, start_date, domain=domain, owner_id=owner_id)

if __name__ == "__main__":
    main()
