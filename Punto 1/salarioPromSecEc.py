from mrjob.job import MRJob

class salarioPromSecEc(MRJob):

    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            sececon = filing[1]
            salario = float(filing[2])
            yield sececon, salario

    def reducer(self, key, values):
        salarioTotal = 0
        count = 0

        for salario in values:
            salarioTotal += salario
            count += 1

        promedio = salarioTotal / count

        yield key, promedio

if __name__ == '__main__':
    salarioPromSecEc.run()