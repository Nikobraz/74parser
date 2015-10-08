# -*- coding: utf-8 -*-
import urllib.request
import re
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
        min_salary = ''
        max_salary = ''
        salary = ''
        text_salary = cols[1].find('div', class_='job_price').text.strip().replace(' ', '')
        text_salary = re.findall(r'\d{5}', text_salary)
        if text_salary.__len__() == 2:
            min_salary = text_salary[0]
            max_salary = text_salary[1]
            salary = (int(min_salary) + int(max_salary))/2
        elif text_salary.__len__() == 1:
            salary = text_salary[0]
        else:
            salary = 0
        if salary == 0:
            countzero += 1

        vac.append({
            'title': title,
            'link': link,
            'min.salary': min_salary,
            'max.salary': max_salary,
            'salary': int(salary),
        })

    medsal = 0
    for vacancy in vac:
        print(vacancy)
        medsal += vacancy['salary']
    print('Средняя зарплата по больнице:', int(medsal / (len(vac) - countzero)), 'рублей')


def main():
    parse(get_data('http://74.ru/job/vacancy/?Where%5B%5D=1&Search=1&Query=%F1%E8%F1%F2%E5%EC%ED%FB%E9+%E0%E4%EC%E8%ED'
                   '%E8%F1%F2%F0%E0%F2%EE%F0&SalaryMin=%C7%E0%F0%EF%EB%E0%F2%E0+%EE%F2%2C+%F0%F3%E1&BranchID='))


if __name__ == '__main__':
    main()
