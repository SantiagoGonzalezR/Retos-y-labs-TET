from mrjob.job import MRJob
from datetime import datetime

class listaAcciones(MRJob):

    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            comp = filing[0]
            precio = float(filing[1])
            fecha = datetime.strptime(filing[2].strip(), '%Y-%m-%d')
            fechStr = fecha.strftime('%Y-%m-%d')
            yield comp, (fechStr, precio)

    def reducer(self, comp, values):
        sorted_values = sorted(values, key=lambda x: x[0])
        precioAnt = None
        incremento = True

        for fecha, precio in sorted_values:
            if precioAnt is not None and precio < previous_price:
                incremento = False
                break

            previous_price = precio

        if incremento:
            yield comp, 'Sube/Mantiene estable'

if __name__ == '__main__':
    listaAcciones.run()