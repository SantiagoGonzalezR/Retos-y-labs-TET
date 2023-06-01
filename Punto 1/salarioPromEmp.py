from mrjob.job import MRJob

class salarioPromEmp(MRJob):

    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            idemp = filing[0]
            salario = float(filing[2])
            yield idemp, salario

    def reducer(self, key, values):
        totalSalarios = 0
        count = 0

        for salario in values:
            totalSalarios += salario
            count += 1

        yield key, totalSalarios / count

if __name__ == '__main__':
    salarioPromEmp.run()