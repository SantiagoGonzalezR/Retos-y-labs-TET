from mrjob.job import MRJob
from mrjob.step import MRStep

class menorDia(MRJob):
    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            fecha = filing[4]
            yield fecha, 1

    def reducer(self, key, values):
        vistas = sum(values)
        yield None, (vistas, key)

    def encontrarMin(self, _, fechas_y_visualizaciones):
        vistasMin = float('inf')
        fechaMin = None
        for vistas, fecha in fechas_y_visualizaciones:
            if vistas < vistasMin:
                vistasMin = vistas
                fechaMin = fecha
        yield fechaMin, vistasMin

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.encontrarMin)
        ]

if __name__ == '__main__':
    menorDia.run()