#!/usr/bin/env python

from selenium import webdriver
import chromedriver_binary
from bs4 import BeautifulSoup
import re
import subprocess

# TODO there are lots of['a', 'b', 'c', 'd']


class AtCoderAutoTester():
    def __init__(self):
        self.contest_id = -1
        self.samples = {}
        pass

    def start(self):
        print("==========================\n" +
              "=AAT(AtCoder Auto Tester)=\n" +
              "==========================\n")
        print("\nWelcome to AAT(AtCoder Auto Tester)\n" +
              "It currently support only AtCoderBeginnersContest.\n" +
              "After enter contest id, input command below. Thank you!\n")

        self.print_manual()

        # TODO input validation
        self.contest_id = input(
            "Please input ABC-contest id(like 123 for ABC123) :")
        self.contest_id = int(self.contest_id)

        self.samples = self.scrape_sample()

        while(True):
            cmd = input("Command :")
            if cmd in ['a', 'b', 'c', 'd']:
                self.compile(cmd)
                self.test(cmd)
            elif cmd == 'm':
                self.print_manual()
            elif cmd == 'q':
                break
            else:
                print("Error Input Correct Command")

        print('Quit')

    def scrape_sample(self):
        print("Scraping")

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)

        base_url = 'https://atcoder.jp/contests/abc{0}/tasks/abc{0}_'.format(
            str(self.contest_id))

        print("Parsing")
        samples = {}
        for problem in ['a', 'b', 'c', 'd']:
            target_url = base_url + problem
            driver.get(target_url)

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            pre_samples = [e.text for e in soup.find_all(
                id=re.compile('pre-sample\d+'))]

            sample_pairs = [{"input": pre_samples[i], "output":pre_samples[i+1]}
                            for i in range(0, len(pre_samples), 2)]

            if sample_pairs == []:
                print(
                    "Failed to Scrape test cases\n Please make sure this is correct id(number)")
                exit(1)

            samples.update({problem: sample_pairs})

        print("Preparation Done")
        driver.quit()
        return samples

    def compile(self, problem):
        if problem in ['a', 'b', 'c', 'd']:
            print("Compiling")
            subprocess.call('g++ {0}.cpp -o {0}'.format(problem).split(' '))
        else:
            print("Error")

    def test(self, problem):
        ac_flag = True
        for sample in self.samples[problem]:
            rtn = subprocess.Popen(
                "./{}".format(problem),  stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            rtn = rtn.communicate(sample["input"].encode())[0].decode('utf-8')

            if rtn.strip() == sample["output"].strip():
                print('OK')
            else:
                print("FAILED")
                ac_flag = False

        if(ac_flag):
            print("====\n" +
                  "=AC=\n" +
                  "====\n")
        else:
            print("====\n" +
                  "=WA=\n" +
                  "====\n")

    def print_manual(self):
        print("---COMMAND MANUAL---\n" +
              "- a : Test a.cpp file for problem A -\n" +
              "- b : Test b.cpp file for problem b -\n" +
              "- c : Test c.cpp file for problem C -\n" +
              "- d : Test d.cpp file for problem D -\n" +
              "- q : Quit -\n" +
              "- m : Print Manual -\n")


if __name__ == "__main__":
    aat = AtCoderAutoTester()
    aat.start()
