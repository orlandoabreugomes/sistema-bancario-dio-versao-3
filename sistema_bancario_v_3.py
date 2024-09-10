# Programa para fazer depósitos, saques e imprimir extratos, utilizando POO:

from abc import ABC, abstractmethod

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):

        # Verifica se a conta já está associada a este cliente:
        if conta in self._contas:
            print(f" @@@ A conta {conta._numero} já está associada ao cliente. @@@ ")
        else:
            # Adiciona a conta à lista do cliente
            self._contas.append(conta)

class PessoaFisica(Cliente):
    # Dicionário que armazena todos os clientes com o CPF como chave:
    usuarios = {}

    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    # Médoto para coletar os dados de um novo usuário:
    @classmethod
    def obter_dados(cls):

        # Solicita o CPF:
        cpf = input("informe o CPF (somente números): ")

        # Verfica se possui somente números:
        if not cpf.isdigit():
            print(f"\n@@@ Erro: O CPF deve ter somente números. @@@\n")
            return None
                  
        # Verifica se já existe um usuário com esse CPF:
        if cls.buscar_usuarios(cpf):
            print(f"\n@@@ Erro: Já existe um usuário com o CPF: {cpf}. @@@\n")
            return None
        
        # Obtém os demais dados do usuário:
        nome = input("Informe o nome: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, número - bairro - cidade / sigla estado): ")

        # Retorna os valores solicitados:
        return cpf, nome, data_nascimento, endereco
    
    # Método para buscar um usuário com base no CPF:
    @classmethod
    def buscar_usuarios(cls, _cpf):
        return cls.usuarios.get(_cpf, None)
    
    # Método para criar novo usuário:
    @classmethod
    def criar_usuario(cls):
        dados = cls.obter_dados()
        if dados is None:
            return None
        cpf, nome, data_nascimento, endereco = dados
        novo_usuario = cls(cpf, nome, data_nascimento, endereco)
        cls.usuarios[cpf] = novo_usuario
        print(f"\n=== Usuário {nome} criado com sucesso. ===\n")
        return novo_usuario

class Transacao(ABC):
    # Método para registrar a transação:
    @abstractmethod
    def registrar_transacao(self, conta):
        pass

class Conta(Transacao):
    # Dicionário para armazenar todas as contas criadas:
    contas = {}

    # Contador para gerar o número das contas:
    numero_conta_atual = 1

    # Constante para a agência padrão:
    AGENCIA = "0001"

    def __init__(self, cliente, agencia=AGENCIA):
        self._saldo = 0
        self._numero = Conta.numero_conta_atual
        self._agencia = agencia
        self._cliente = cliente
        self._historico = ["\n"]
        
        # Adicionar a conta ao dicionário de contas da classe Conta:
        Conta.contas[self._numero] = self

        # Incrementar o número da próxima conta a ser criada:
        Conta.numero_conta_atual += 1

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    @classmethod
    def criar_conta(cls):
        # Solicita o CPF do cliente:
        cpf = input("Informe o CPF (somente números): ")

        # Verfica se possui somente números:
        if not cpf.isdigit():
            print(f"\n@@@ Erro: O CPF deve ter somente números. @@@\n")
            return None
        
        # Busca o cliente pelo CPF:
        cliente = PessoaFisica.buscar_usuarios(cpf)
                
        # Verifica se já existe o cliente:
        if cliente is None:
            print(f"\n@@@ Erro: Cliente com o {cpf} não foi encontrado. @@@\n")
            return None
    
        # Cria numa nova conta para o cliente fornecido:
        nova_conta = ContaCorrente(cliente)
        # Adicona a conta ao cliente:
        cliente.adicionar_conta(nova_conta)

        print(f"\n === Conta {nova_conta._numero} criada com sucesso para o cliente. ===")

        return True

    # Registra a transação no histórico
    def registrar_transacao(self, registro):
        # Adiciona transação no histórico:
        self._historico.append(registro)

    # Realiza o saque da conta e registra a transação:
    def sacar(self, valor, limite_valor, limite_saques):

        if valor <= 0:
            print(f" @@@ Erro: O valor do saque deve ser positivo. @@@ ")
            return None

        if valor > self._saldo:
            print(f" @@@ Erro: Saldo insuficiente. @@@ ")
            return None
        
        if valor > limite_valor:
            print(f" @@@ Erro: O valor é superior ao valor limite: R$ {limite_valor:.2f}. @@@ ")
            return None
        
        numero_saques = sum(item.count("Saque") for item in self._historico)
        if numero_saques >= limite_saques:
            print(f" @@@ Erro: Número de saques superior ao limite: {limite_saques}. @@@ ")
            return None
        
        self._saldo -= valor
        self.registrar_transacao(f"Saque:    R$ {valor:.2f}\n")
        print(f"\n === Saque realizado com sucesso. ===")

    # Realiza o depósito na conta e registra a transação:
    def depositar(self, valor):

        if valor <= 0:
            print(f" @@@ Erro: O valor do depósito deve ser positivo. @@@ ")
            return None
        
        self._saldo += valor
        self.registrar_transacao(f"Depósito: R$ {valor:.2f}\n")
        print(f"\n === Depósito realizado com sucesso. ===")


class ContaCorrente(Conta):
    # Constante que definem os saques:
    LIMITE_SAQUES = 2
    LIMITE_VALOR = 500

    def __init__(self, cliente, limite = LIMITE_VALOR, limite_saques = LIMITE_SAQUES):
        super().__init__(cliente)
        self._limite = limite
        self._limite_saques = limite_saques

def fazer_transacao(tipo):
        
    # Solicita o CPf da conta:
    cpf = input("Informe o CPF (somente númeoros): ")

    # Verfica se possui somente números:
    if not cpf.isdigit():
        print(f"\n@@@ Erro: O CPF deve ter somente números. @@@\n")
        return None
    
    # Detemina a conta do cliente pelo CPF:
    usuario = PessoaFisica.buscar_usuarios(cpf)

    # Envia mensagem de erro se não existir o usuário desse CPF:
    if usuario == None:
        print(f" @@@ Erro: CPF não cadastrado. @@@ ")
        return None
    
    # Envia mensagem de erro se não existir conta para esse CPF:
    if usuario._contas == []:
        print(f" @@@ Erro: CPF não tem conta. @@@ ")
        return None

    conta = usuario._contas[0]

    # Realiza a transação bancária:
    if tipo == "sacar":

        # Solicita o valor do saque:
        valor = float(input("Informe o valor do saque: "))

        # Realiza o saque:
        conta.sacar(valor, conta._limite, conta._limite_saques)

    else:
        # Solicita o valor do depósito:
        valor = float(input("Informe o valor do saque: "))

        # Realiza o depósito:
        conta.depositar(valor)

def exibir_extrato():
        
    # Solicita o CPf da conta:
    cpf = input("Informe o CPF (somente númeoros): ")

    # Verfica se possui somente números:
    if not cpf.isdigit():
        print(f"\n@@@ Erro: O CPF deve ter somente números. @@@\n")
        return None
    
    # Detemina a conta do cliente pelo CPF:
    usuario = PessoaFisica.buscar_usuarios(cpf)

    # Envia mensagem de erro se não existir o usuário desse CPF:
    if usuario == None:
        print(f" @@@ Erro: CPF não cadastrado. @@@ ")
        return None
    
    # Envia mensagem de erro se não existir conta para esse CPF:
    if usuario._contas == []:
        print(f" @@@ Erro: CPF não tem conta. @@@ ")
        return None

    conta = usuario._contas[0]    

    extrato = "".join(conta._historico)

    print("\n================ EXTRATO ================")
    print("=== Não foram realizadas movimentações. ===" if extrato == "\n" else extrato)
    print(f"\nSaldo:    R$ {conta._saldo:.2f}")
    print("==========================================")

def main():

    while True:
        opcao = menu()

        if opcao.lower() == "d":
            fazer_transacao("depositar")
            
        elif opcao.lower() == "s":
            fazer_transacao("sacar")

        elif opcao.lower() == "e":
            exibir_extrato()
            
        elif opcao.lower() == "nc":
            # cria uma nova conta:
            Conta.criar_conta()

        elif opcao.lower() == "nu":
           # Registra um novo usuário:
           PessoaFisica.criar_usuario()

           
        elif opcao.lower() == "q":
            break
        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@\n")

# Define o Menu principal e retorna o valor da opção escolhida:
def menu():
    menu = """

    [d]  Depositar
    [s]  Sacar
    [e]  Extrato
    [nc] Nova conta
    [nu] Novo usuário
    [q]  Sair

=> """
    opcao = input(menu)
    return opcao

# Inicia a função principal:
main()