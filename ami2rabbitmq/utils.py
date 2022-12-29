def endpoint_parse(channel):
    posicao_final = channel.rfind('-')
    return channel[:posicao_final]

def queue_parse(queue):
    remover = ['Queue:']

    for item in remover:
        queue = queue.replace(item, '')
    
    partes_nome = queue.split('_')

    return f'{partes_nome[0]}_{partes_nome[1]}'