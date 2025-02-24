from logging import getLogger, basicConfig, DEBUG, FileHandler


logger = getLogger()


FORMAT = '%(asctime)s : %(name)s : %(levelname)s : %(message)s'

basicConfig(level=DEBUG, format=FORMAT, filename='report.log', encoding='utf-8', filemode='w')
