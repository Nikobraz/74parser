# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup


def get_data(url):
    responce = urllib.request.urlopen(url)
    return responce.read()


def parse(html):
    vac = []
    vac.clear()
    countzero = 0

    soup = BeautifulSoup(html)
    table = soup.find('table', class_='table2')
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        title = cols[1].a.text
        link = cols[1].a['href']
        text_salary = cols[1].find('div', class_='job_price').text.strip()
        min_salary = ''
        max_salary = ''
        salary = ''
        print(text_salary)
        if text_salary.find('от') == 0:
            min_salary = int(text_salary.replace(' ', '')[2:8])
        if text_salary.find('до') != -1:
            max_salary = text_salary[text_salary.find('до')+3:text_salary.find('до ')+9]
            max_salary = int(max_salary.replace(' ', ''))
        if text_salary.find('от') == -1 and text_salary.find('до') == -1:
            salary = text_salary.replace(' ', '')[0:5]

            if salary.isdigit():
                salary = int(salary)
            else:
                salary = 0
        if min_salary == 0 or max_salary == 0:
            salary = min_salary + max_salary
        if int(min_salary) > 0 and int(max_salary) > 0:
            salary = (min_salary + max_salary) / 2
        if salary == 0:
            countzero += 1

        vac.append({
            'title': title,
            'link': link,
            'min.salary': min_salary,
            'max.salary': max_salary,
            'salary': salary,
        })

    medsal = 0
    for vacancy in vac:
        print(vacancy)
        medsal += vacancy['salary']
    print('Средняя зарплата по больнице:', int(medsal / (len(vac) - countzero)), 'рублей')
'''        if not (min_salary and min_salary.string):
            salary = '0'
            countzero += 1
        else:
            min_salary = min_salary.string
            print(min_salary)
        vac.append({
            'title': title,
            'link': link,
            'salary': int(min_salary.replace(' ', '')),
        })'''


def main():
    parse(get_data('http://74.ru/job/vacancy/?Where%5B%5D=1&Search=1&Query=%F1%E8%F1%F2%E5%EC%ED%FB%E9+%E0%E4%EC%E8%ED'
                   '%E8%F1%F2%F0%E0%F2%EE%F0&SalaryMin=%C7%E0%F0%EF%EB%E0%F2%E0+%EE%F2%2C+%F0%F3%E1&BranchID='))


if __name__ == '__main__':
    main()
