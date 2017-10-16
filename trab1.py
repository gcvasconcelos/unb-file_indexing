# Parâmetros: um array, e duas posições no array
# Troca dois elementos de posição no array
def troca_valores(array, i, j):
    array[i], array[j] = array[j], array[i]

# Parâmetros: um array, sua posição final e inicial
# Transforma um array em um heap
def heapify(array, comeco, fim):
    esquerda = 2 * comeco + 1
    direita = 2 * (comeco + 1)
    maximo = comeco
    if (esquerda < fim) and (array[comeco] < array[esquerda]):
        maximo = esquerda
    if direita < fim and array[maximo] < array[direita]:
        maximo = direita
    if maximo != comeco:
        troca_valores(array, comeco, maximo)
        heapify(array, maximo, fim)
    return

# Ordena um array por meio de um heapsort
def heapsort(array):
    fim = len(array)
    comeco = fim // 2 - 1
    for i in range(comeco, -1, -1):
        heapify(array, i, fim)
    for i in range(fim - 1, 0, -1):
        troca_valores(array, i, 0)
        heapify(array, 0, i)
    return

# Variável global que conta a quantidade de registros
num_registros = 0

# A partir de um arquivio de registros, separa os campos e os coloca nas devidas variáveis
# de uma lista de registros 
def inicializa_registros(arquivo):
    global num_registros
    registros = []
    for linha in arquivo:
        registro = {}
        dados = linha.split()
        registro['matric'] = dados[0]
        registro['nome'] = ' '.join(dados[1:-3])
        registro['op'] = dados[-3]
        registro['curso'] = dados[-2]
        registro['turma'] = dados[-1]
        registros.append(registro)
        num_registros += 1
    return registros

# Gera chaves primárias de uma lista de registros e cria uma lista com elas e suas posições
def inicializa_indices(arq_indices, registros):
    indices = []
    posicao = 0
    for registro in registros:
        indice = {}
        chave_primaria = registro['matric'] + '#' + registro['nome']
        chave_primaria = chave_primaria[0:30]
        indice['pk'] = chave_primaria
        indice['posicao'] = posicao
        indices.append(indice)
        posicao += 1
        arq_indices.write(indice['pk'] + ' ' * (2 + (30 - len(indice['pk']))) + str(indice['posicao']) + '\n')
    return indices

# Ordena os índices por matrícula
def ordena_indices(arq_indices, indices):
    arq_indices.seek(0, 0)
    heapsort(indices)
    for indice in indices:
        arq_indices.write(indice['pk'] + ' ' * (2 + (30 - len(indice['pk']))) + str(indice['posicao']) + '\n')
    return


def opcoes_secundario(registros, ind_secundario):
    opcoes = []
    for registro in registros:
        if registro[ind_secundario] not in opcoes:
            opcoes.append(registro[ind_secundario])
    return opcoes

# Encontra um registro por meio da chave primária
def busca_registro(chave_primaria, ind_secundario, registros):
    for registro in registros:
        pk = registro['matric'] + '#' + registro['nome']
        pk = pk[0:30]
        if chave_primaria == pk:
            return registro[ind_secundario]
    return None

# Cria o arquivo de índices secundários usando os registros e os índices secundários
def inicializa_indice_secundario(arq_secundario, registros, indices, ind_secundario):
    opcoes = opcoes_secundario(registros, ind_secundario)
    head = []
    for i in range(len(opcoes)):
        head.append(-1)

    for indice in indices:
        sk = busca_registro(indice['pk'], ind_secundario, registros)
        for opcao in opcoes:
            if sk == opcao:
                foo = opcoes.index(opcao)
                arq_secundario.write(
                    str(indice['posicao']) + '\t' + indice['pk'] + ' ' * (2 + (30 - len(indice['pk']))) + str(
                        head[foo]) + '\n')
                head[foo] = indice['posicao']
    return


def printa_arquivo(arquivo):
    for linha in arquivo:
        print(linha)
    return

# Adiciona um novo registro a todos os arquivos, mudando as listas invertidas dos índices secundários
def adicionar_registro(arq_registros, arq_indices, arq_secundario_op, arq_secundario_turma, registros, indices,
                       novo_registro):
    global num_registros
    registros.append(novo_registro)
    arq_registros.write(# escreve o novo registro no arquivo contendo todos
        '\n' + novo_registro['matric'] + ' ' + novo_registro['nome'] + ' ' * (41 - len(novo_registro['nome'])) +
        novo_registro['op'] + ' ' * 4 +
        novo_registro['curso'] + ' ' * 9 + novo_registro['turma'])

    indice = {}
    chave_primaria = novo_registro['matric'] + '#' + novo_registro['nome']
    chave_primaria = chave_primaria[0:30]
    indice['pk'] = chave_primaria
    indice['posicao'] = num_registros
    num_registros += 1
    indices.append(indice)
    ordena_indices(arq_indices, indices)

    # Atualiza os índices secundários
    inicializa_indice_secundario(arq_secundario_op, registros, indices, 'op')
    inicializa_indice_secundario(arq_secundario_turma, registros, indices, 'turma')
    return

# Remove um registro de todos os arquivos a partir por meio da matrícula
def remover_registros(arq_registros, arq_indices, arq_secundario_op, arq_secundario_turma, registros, indices, matric_remover):
    posicao_remover = -1
    for i in range(0, len(registros)):
        if registros[i]['matric'] == matric_remover:
            posicao_remover = i
    if posicao_remover == -1:# verifica se o registro está no arquivo
        print ('Registro nao encontrado')
    else:# remoção do registro e do índice
        registros.pop(posicao_remover)
        indices.pop(posicao_remover)
    final = i-1
    i = 0
    # Atualiza os registros
    for registro in registros:
        arq_registros.write(
            registro['matric'] + ' ' + registro['nome'] + ' ' * (41 - len(registro['nome'])) +
            registro['op'] + ' ' * 4 + registro['curso'] + ' ' * 9 + registro['turma'])
        if i != final:
            arq_registros.write('\n')
        i += 1
    i = 0
    # Atualiza os índices primários
    for indice in indices:
        arq_indices.write(indice['pk']+str(indice['posicao'])+'\n')
        if i != final:
            arq_indices.write('\n')
        i += 1
        # Atualiza os índices secundários
    inicializa_indice_secundario(arq_secundario_op, registros, indices, 'op')
    inicializa_indice_secundario(arq_secundario_turma, registros, indices, 'turma')
    return

# Inicialização dos registros
arq_registros1 = open('benchmarks/lista1.txt', 'r')
registros = inicializa_registros(arq_registros1)
arq_registros1.close()

# Criação dos índices primários
arq_indices1 = open('indice_lista1.ind', 'w+')
indices = inicializa_indices(arq_indices1, registros)
ordena_indices(arq_indices1, indices)
arq_indices1.close()

# Criação dos índices secundários
secundario_op = open('op_lista1.ind', 'w+')
secundario_turma = open('turma_lista1.ind', 'w+')
inicializa_indice_secundario(secundario_op, registros, indices, 'op')
inicializa_indice_secundario(secundario_turma, registros, indices, 'turma')
secundario_op.close()
secundario_turma.close()

print('\n\tMenu')
print('1.\tVisualizar arquivos')
print('2.\tIncluir registro')
print('3.\tExcluir registro')
print('4.\tAtualizar registro')
opcao_menu = input()
if opcao_menu == 1:
    print('\n1\tArquivo de dados')
    print('2\tArquivo de indices primarios')
    print("3\tArquivo de indice secundario 'OP'")
    print("4\tArquivo de indice secundario 'TURMA'\n")
    escolha = input()
    if escolha == 1:
        arquivo = open('benchmarks/lista1.txt', 'r')
        printa_arquivo(arquivo)
        arquivo.close()
    elif escolha == 2:
        arquivo = open('indice_lista1.ind', 'r')
        printa_arquivo(arquivo)
        arquivo.close()
    elif escolha == 3:
        arquivo = open('op_lista1.ind', 'r')
        printa_arquivo(arquivo)
        arquivo.close()
    elif escolha == 4:
        arquivo = open('turma_lista1.ind', 'r')
        printa_arquivo(arquivo)
        arquivo.close()
    else:
        print('Opcao invalida')
elif opcao_menu == 2:
    novo_registro = {}
    novo_registro['matric'] = raw_input('Digite a matricula: ')
    novo_registro['nome'] = raw_input('Digite o nome: ')
    novo_registro['op'] = raw_input('Digite o OP: ')
    novo_registro['curso'] = raw_input('Digite a curso: ')
    novo_registro['turma'] = raw_input('Digite a turma: ')

    arq_registros = open('benchmarks/lista1.txt', 'r')
    printa_arquivo(arq_registros)

    arq_registros = open('benchmarks/lista1.txt', 'a')
    arq_indices = open('indice_lista1.ind', 'w+')
    arq_secundario_op = open('op_lista1.ind', 'a')
    arq_secundario_turma = open('turma_lista1.ind', 'a')
    adicionar_registro(arq_registros, arq_indices, arq_secundario_op, arq_secundario_turma, registros, indices,
                       novo_registro)
    arq_registros = open('benchmarks/lista1.txt', 'r')
    printa_arquivo(arq_registros)
    arq_registros.close()
    arq_indices.close()
    arq_secundario_op.close()
    arq_secundario_turma.close()
elif opcao_menu == 3:
    arquivo = open('indice_lista1.ind', 'r')
    printa_arquivo(arquivo)
    arquivo.close()

    print ('Digite a matricula do registro a ser removido')
    matricula_remover = str(raw_input())

    arq_registros = open('benchmarks/lista1.txt', 'w')
    arq_indices = open('indice_lista1.ind', 'w+')
    arq_secundario_op = open('op_lista1.ind', 'a')
    arq_secundario_turma = open('turma_lista1.ind', 'a')
    remover_registros(arq_registros, arq_indices, arq_secundario_op, arq_secundario_turma, registros, indices, matricula_remover)
    arq_registros = open('benchmarks/lista1.txt', 'r')
    printa_arquivo(arq_registros)
    arq_registros.close()
    arq_indices.close()
    arq_secundario_op.close()
    arq_secundario_turma.close()
elif opcao_menu == 4:
    arquivo = open('indice_lista1.ind', 'r')
    printa_arquivo(arquivo)
    arquivo.close()

    print ('Qual matricula deseja atualizar?')
    matric_atualizar = raw_input()

    posicao_atualizar = -1
    for i in range(0, len(registros)):
        if registros[i]['matric'] == matric_atualizar:
            posicao_atualizar = i
    if posicao_atualizar == -1:# verificação da existência do registro
        print ('Registro nao encontrado')
    else:
        print (registros[posicao_atualizar]['matric'] + registros[posicao_atualizar]['nome'] +
                           registros[posicao_atualizar]['op'] + registros[posicao_atualizar]['curso'] +
                           registros[posicao_atualizar]['turma'])
        print ('O que deseja atualizar?')
        print ('1\tMatricula')
        print ('2\tNome')
        print ('3\tOpcao')
        print ('4\tCurso')
        print ('5\tTurma')
        campo_atualizar = input()
        print ('Digite o novo dado:')
        dado = str(raw_input())
        new_registro = {}
        new_registro['matric'] = registros[posicao_atualizar]['matric']
        new_registro['nome'] = registros[posicao_atualizar]['nome']
        new_registro['op'] = registros[posicao_atualizar]['op']
        new_registro['curso'] = registros[posicao_atualizar]['curso']
        new_registro['turma'] = registros[posicao_atualizar]['turma']
        if campo_atualizar == 1:# atualiza o dado escolhido com a informação dada
            new_registro['matric'] = dado
        elif campo_atualizar == 2:
            new_registro['nome'] = dado
        elif campo_atualizar == 3:
            new_registro['op'] = dado
        elif campo_atualizar == 4:
            new_registro['curso'] = dado
        elif campo_atualizar == 5:
            new_registro['turma'] = dado

        arq_registros = open('benchmarks/lista1.txt', 'w')
        arq_indices = open('indice_lista1.ind', 'w+')
        arq_secundario_op = open('op_lista1.ind', 'w')
        arq_secundario_turma = open('turma_lista1.ind', 'w')
        remover_registros(arq_registros, arq_indices, arq_secundario_op, arq_secundario_turma, registros, indices,
                          matric_atualizar)
        arq_registros = open('benchmarks/lista1.txt', 'a')
        arq_indices = open('indice_lista1.ind', 'w+')
        arq_secundario_op = open('op_lista1.ind', 'w')
        arq_secundario_turma = open('turma_lista1.ind', 'w')
        adicionar_registro(arq_registros, arq_indices, arq_secundario_op, arq_secundario_turma, registros, indices,
                           new_registro)
        arq_registros = open('benchmarks/lista1.txt', 'r')
        printa_arquivo(arq_registros)
        arq_registros.close()
        arq_indices.close()
        arq_secundario_op.close()
        arq_secundario_turma.close()
