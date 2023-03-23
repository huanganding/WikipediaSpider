import csv
import os

import pandas as pd
import scrapy


class WikiSpider(scrapy.Spider):
    name = "wiki"

    def start_requests(self):
        import_csv = self.settings['IMPORT_CSV']
        export_xlsx = self.settings["EXPORT_XLSX"]
        self.export_xlsx = export_xlsx
        self.extract_result_text = self.settings['EXTRACT_RESULT_TEXT_FUNC']
        self.import_csv_n_items = int(self.settings['IMPORT_CSV_N_ITEMS'])

        print('\n==== 维基百科抓取程序 ====\n')

        print('设置(settings.py)：')
        print(f'输入CSV: {import_csv}')
        print(f'输出XLSX: {export_xlsx}')
        print()

        if not os.path.exists(import_csv):
            print('错误：输入文件不存在。')
        if os.path.exists(export_xlsx):
            print('警告:输出文件已存在，将覆盖。')
        print()

        print('注意事项：')
        input(
            """- 请确认输入文件存在。
- 请确认已备份好输出xlsx文件且未在excel打开，若已打开关闭，抓取过程中也不要打开，以免保存失败！！
- 请确认可以正常访问维基百科。
- 若需要提前结束，请只按一次Ctrl+C，等待程序保存已抓取内容并自动退出。

确认以上提示后回车继续:""")
        print('已开始..')

        names = []
        results = []
        urls = []
        with open(import_csv, 'r') as f:
            reader = csv.DictReader(f)
            for kv in reader:
                name = kv['name']
                names.append(name)
                results.append(None)
                urls.append(None)
        if self.import_csv_n_items:
            names = names[0:self.import_csv_n_items]
            results = results[0:self.import_csv_n_items]
            urls = urls[0:self.import_csv_n_items]
        self.names = names
        self.results = results
        self.urls = urls
        print(f'将抓取 {len(names)} 项..')

        for name_index, name in enumerate(names):
            wiki_name_in_url = name.replace(' ', '_')
            wiki_url = 'https://en.wikipedia.org/wiki/' + wiki_name_in_url
            yield scrapy.Request(wiki_url, cb_kwargs=dict(name_index=name_index))

    def parse(self, response, name_index=0):
        name = self.names[name_index]
        url = response.url
        if response.status == 200:
            result = self.extract_result_text(response)
            # print()
            # print(url)
            # print(result)
            # print()
        else:
            result = 'None'
        self.results[name_index] = result
        self.urls[name_index] = url
        yield dict(name_index=name_index, name=name, result=result, url=url)

    def closed(self, reason):
        df = pd.DataFrame({'name': self.names, 'result': self.results, 'url': self.urls})
        while True:
            try:
                open(self.export_xlsx, 'w')
            except:
                input('错误：文件被占用！请关闭后回车：')
            else:
                break
        df.to_excel(self.export_xlsx)
        print('已保存输出文件。')
