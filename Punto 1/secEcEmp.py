from mrjob.job import MRJob

class secEcEmp(MRJob):

    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            idemp = filing[0]
            sececon = filing[1]
            yield idemp, sececon

    def reducer(self, key, values):
        sececonsUnicos = set(values)
        yield key, len(sececonsUnicos)

if __name__ == '__main__':
    secEcEmp.run()