import json

parsePath = [
    '/home/edmond/douban/requests/parse.json',
    '/home/edmond/douban/scrapyInfo/InfoJson/parse1.json',
    '/home/edmond/douban/scrapyInfo/InfoJson/parse2.json',
    '/home/edmond/douban/scrapyInfo/parse.json'
]

rawPath = [
    '/home/edmond/douban/requests/raw.json',
    '/home/edmond/douban/scrapyInfo/InfoJson/raw1.json',
    '/home/edmond/douban/scrapyInfo/InfoJson/raw2.json',
    '/home/edmond/douban/scrapyInfo/raw.json'
]


def together(paths, save):
    data = []
    for path in paths:
        with open(path, 'r', encoding='utf-8') as f:
            data.extend(json.load(f))
    print(len(data))
    with open(save, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    together(parsePath, '/home/edmond/douban/InfoJson/parse.json')
    together(rawPath, '/home/edmond/douban/InfoJson/raw.json')
