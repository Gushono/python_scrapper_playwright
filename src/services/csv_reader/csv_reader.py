import csv


class CSVReader:
    @staticmethod
    def read_urls_from_csv(file_path: str):
        urls = []
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                url = row.get('g2crowdurl')
                if url:
                    urls.append(url)
        return urls
