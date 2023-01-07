""" 
from django.db import models
from django.utils.html import mark_safe
from cpf_field.models import CPFField


##########################################################
class User(AbstractUser):
    class Types(models.TextChoices):
        SPY = "SPY", "Spy"
        DRIVER = "DRIVER", "Driver"

    type = models.CharField(_("Type"), max_length=50, choices=Types.choices, default=Types.SPY)

    name = models.CharField(_("User Name"), blank=True, max_length=255 )

    def get_absolute_url(self):
        return reverse("users:details", kwargs={"username":self.username})

class SpyManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.SPY)

class DriverManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.DRIVER)

#Proxy models do not create new tables
class Spy(User):
    objects = SpyManager()
    
    class Meta: 
        proxy = True

    def whisper(self):
        return "whisper"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.SPY
        
        return super().save(*args, **kwargs)

class Driver(User):
    objects = DriverManager()
    class Meta: 
        proxy = True

    def accelerate(self):
        return "accelerating"


    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.DRIVER

############################################################

class TenantSystem(models.Model):
    system_tenant_name = models.CharField(max_length=100, null=False)
    system_tenant_logo = models.ImageField(
        upload_to='tenant_company_logos/%Y/%m/%d/', null=True, blank=True)

    def system_tenant_logo_preview(self):
        from django.utils.html import escape
        if (self.system_tenant_logo):
            return mark_safe(u'<img src="%s" width="32" height="32"/>' % escape(self.system_tenant_logo.url))
        else:
            return mark_safe('<img src="" />')
            
    system_tenant_logo_preview.short_description = 'System Tenant Logo Preview'
    system_tenant_logo_preview.allow_tags = True

    system_description = models.CharField(max_length=255, null=False)
    authorized_by = models.CharField(max_length=15, null=False, default="FEALVES")
    ativo = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    oper = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}: {self.system_tenant_name} [Ativo: {self.ativo}]"


class CepBROfficial(models.Model):
    cep_official = models.CharField(max_length=8, null=True)
    estado_official = models.CharField(max_length=2, null=True)
    cidade_official = models.CharField(max_length=100, null=True)
    bairro_official = models.CharField(max_length=100, null=True)
    endereco_official = models.CharField(max_length=120, null=True)


"""     def __str__(self):
        return f"{self.id}|{self.cep_official}|{self.endereco_official}|{self.bairro_official}|{self.cidade_official}|\
        {self.estado_official}" """


class Endereco(models.Model):
    RESIDENCIA = 'Residencial'
    TRABALHO = 'Trabalho'
    OUTROS = 'Outros'
    RAZAOSOCIAL = 'Razão Social'

    ENDERECO_OPCOES = [
        (RESIDENCIA, 'Residencia (PF)'),
        (TRABALHO, 'Trabalho (PF)'),
        (OUTROS, 'Outros (PF/PJ)'),
        (RAZAOSOCIAL, 'Razao Social (PJ)')
    ]
    tipo_endereco = models.CharField(
        max_length=15, choices=ENDERECO_OPCOES, default=RESIDENCIA)
    # models.ForeignKey(CepBROfficial, on_delete=models.DO_NOTHING, null=True)
    cep = models.CharField(max_length=8,  blank=True, default="")
    estado = models.CharField(max_length=2,  blank=True, default="")
    cidade = models.CharField(max_length=100,  blank=True, default="")
    bairro = models.CharField(max_length=100,  blank=True, default="")
    endereco = models.CharField(max_length=120, blank=True, default="")
    complemento = models.CharField(max_length=120, blank=True, default="")
    complemento2 = models.CharField(max_length=120, blank=True, default="")
    pais = models.CharField(max_length=25,  default='Brasil')
    ponto_referencia = models.CharField(max_length=120, blank=True, default="")
    observacao = models.CharField(max_length=255,  blank=True, default="")
    ativo = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    oper = models.IntegerField(default=0)
    tenant_system = models.ForeignKey(TenantSystem, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.id}: {self.tipo_endereco} | {self.endereco}, {self.complemento}, {self.bairro} | \
        {self.cidade}, {self.estado} - {self.pais}. Cep {self.cep} [Ativo: {self.ativo}]"


class Fone(models.Model):
    RESIDENCIAL = 'Residencial'
    CELULAR = 'Celular'
    WHATSAPP = 'WhatsApp'
    TRABALHO = 'Trabalho'
    OUTROS = 'Outros'
 
    FONE_OPCOES = [
        (RESIDENCIAL, 'Residencial'),
        (CELULAR, 'Celular'),
        (WHATSAPP, 'Whatsapp'),
        (TRABALHO, 'Trabalho'),
        (OUTROS, 'Outros')
    ]
    tipo_fone = models.CharField(
        max_length=15, choices=FONE_OPCOES, default=CELULAR)
    descricao = models.CharField(max_length=100, null=False, blank=True)
    numero = models.CharField(max_length=20, null=False)
    proprietario = models.ForeignKey(
        'PessoaNew', on_delete=models.DO_NOTHING, null=True)
    ativo = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    oper = models.IntegerField(default=0)
    tenant_system = models.ForeignKey(TenantSystem, on_delete=models.PROTECT)


    def __str__(self):
        return f"{self.id}: {self.tipo_fone} | {self.numero} [Ativo: {self.ativo}]"



class Pessoa(models.Model):
    MASCULINO = 'Masculino'
    FEMININO = 'Feminino'
    OUTROS = 'Outros'
    SEXO_OPCOES = [
        (MASCULINO, 'Masculino'),
        (FEMININO, 'Feminino'),
        (OUTROS, 'Outros')
    ]

    CASADO = 'Casado'
    SOLTEIRO = 'Solteiro'
    DIVORCIADO = 'Divorciado'
    VIUVO = 'Viuvo'

    ESTADO_CIVIL_OPCOES = [
        (CASADO, 'Casado(a)'),
        (SOLTEIRO, 'Solteiro(a)'),
        (DIVORCIADO, 'Divorciado(a)'),
        (VIUVO, 'Viuvo(a)')
    ]

    CLIENTE = 'Cliente'
    FUNCIONARIO = 'Funcionario'
    PARCEIRO = 'Parceiro'

    TIPOPESSOA_OPCOES = [
        (CLIENTE, 'Cliente'),
        (FUNCIONARIO, 'Colaborador(a)'),
        (PARCEIRO, 'Parceiro(a), porém não-funcionário(a)')

    ]

    tipo_pessoa = models.CharField(
        max_length=15, choices=TIPOPESSOA_OPCOES, default=SOLTEIRO)
    nome = models.CharField(max_length=100,  blank=True, default="")
    cpf = CPFField(max_length=11,  blank=True, default="")
    identidade = models.CharField(max_length=30,  blank=True, default="")
    sexo = models.CharField(
        max_length=15, choices=SEXO_OPCOES, default=MASCULINO)
    data_nascimento = models.CharField(max_length=10,  blank=True, default="")
    estado_civil = models.CharField(
        max_length=15, choices=ESTADO_CIVIL_OPCOES, default=SOLTEIRO)
    conjuge = models.ForeignKey(
        'self', on_delete=models.DO_NOTHING, null=True, blank=True, default="")
    foto = models.ImageField(
        upload_to='pessoas_fotos/%Y/%m/%d/', null=True, blank=True)

    def foto_preview(self):
        from django.utils.html import escape
        if (self.foto):
            return mark_safe(u'<img src="%s" width="64" height="64"/>' % escape(self.foto.url))
        else:
            return mark_safe('<img src="" />')
    foto.short_description = 'Foto Preview'
    foto.allow_tags = True

    email = models.EmailField(blank=True, default="")
    website = models.URLField(blank=True, default="")
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    fones = models.ManyToManyField(Fone, through="PessoaFisica_Fones")
    def fones_contato(self):
            clist =  ""
            for f in self.fones.all():
                clist += str(f)
                clist += "<br><br>"
       
            return mark_safe(clist)
    ativo = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    oper = models.IntegerField(default=0)
    tenant_system = models.ForeignKey(TenantSystem, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.id}: {self.nome}, Aniversário: {self.data_nascimento} CPF: {self.cpf} Identidade:{self.identidade} Email:{self.email}  [Ativo:{self.ativo}]"

class PessoaNew(models.Model):
    MASCULINO = 'Masculino'
    FEMININO = 'Feminino'
    OUTROS = 'Outros'
    SEXO_OPCOES = [
        (MASCULINO, 'Masculino'),
        (FEMININO, 'Feminino'),
        (OUTROS, 'Outros')
    ]

    CASADO = 'Casado'
    SOLTEIRO = 'Solteiro'
    DIVORCIADO = 'Divorciado'
    VIUVO = 'Viuvo'

    ESTADO_CIVIL_OPCOES = [
        (CASADO, 'Casado(a)'),
        (SOLTEIRO, 'Solteiro(a)'),
        (DIVORCIADO, 'Divorciado(a)'),
        (VIUVO, 'Viuvo(a)')
    ]

    CLIENTE = 'Cliente'
    FUNCIONARIO = 'Funcionario'
    PARCEIRO = 'Parceiro'

    TIPOPESSOA_OPCOES = [
        (CLIENTE, 'Cliente'),
        (FUNCIONARIO, 'Colaborador(a)'),
        (PARCEIRO, 'Parceiro(a), porém não-funcionário(a)')

    ]

    tipo_pessoa = models.CharField(
        max_length=15, choices=TIPOPESSOA_OPCOES, default=SOLTEIRO)
    nome = models.CharField(max_length=100,  blank=True, default="")
    cpf = CPFField(max_length=11,  blank=True, default="")
    identidade = models.CharField(max_length=30,  blank=True, default="")
    sexo = models.CharField(
        max_length=15, choices=SEXO_OPCOES, default=MASCULINO)
    data_nascimento = models.CharField(max_length=10,  blank=True, default="")
    estado_civil = models.CharField(
        max_length=15, choices=ESTADO_CIVIL_OPCOES, default=SOLTEIRO)
    conjuge = models.ForeignKey(
        'self', on_delete=models.DO_NOTHING, null=True, blank=True, default="")
    foto = models.ImageField(
        upload_to='pessoas_fotos/%Y/%m/%d/', null=True, blank=True)

    def foto_preview(self):
        from django.utils.html import escape
        if (self.foto):
            return mark_safe(u'<img src="%s" width="64" height="64"/>' % escape(self.foto.url))
        else:
            return mark_safe('<img src="" />')
    foto.short_description = 'Foto Preview'
    foto.allow_tags = True

    email = models.EmailField(blank=True, default="")
    website = models.URLField(blank=True, default="")
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    
    def fones_contato(self):
            clist =  ""
            for f in self.fones.all():
                clist += str(f)
                clist += "<br><br>"
       
            return mark_safe(clist)
    ativo = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    oper = models.IntegerField(default=0)
    tenant_system = models.ForeignKey(TenantSystem, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.id}: {self.nome}, Aniversário: {self.data_nascimento} CPF: {self.cpf} Identidade:{self.identidade} Email:{self.email}  [Ativo:{self.ativo}]"



class PessoaJuridica(models.Model):
    MEI = 'MEI'
    EP = 'Emp. Individual'
    EIRELI = 'EIRELI'
    LTDA = 'LTDA'
    SOCIEDADE_SIMPLES = 'Soc. Simples'
    SOCIEDADE_ANONIMA = 'Soc. Anônima'
    UNIPESSOAL = 'Unipessoal'

    TIPOEMPRESA_OPCOES = [
        (MEI, 'MEI - Micro Empreendedor Individual'),
        (EP, 'Empresário Individual'),
        (EIRELI, 'EIRELI - Empresa Individual com Responsabilidade LTDA'),
        (LTDA, 'LTDA - Sociedade de Empresárial Limitada'),
        (SOCIEDADE_SIMPLES, 'Sociedade Simples'),
        (SOCIEDADE_ANONIMA, 'S.A. - Sociedade Anônima'),
        (UNIPESSOAL, 'Sociedade Limitada Unipessoal')
    ]

    tipo_empresa = models.CharField(
        max_length=15, choices=TIPOEMPRESA_OPCOES, default=LTDA)
    razao_social = models.CharField(max_length=100, null=True, blank=True, default="")
    nome_fantasia = models.CharField(max_length=100, null=True, blank=True, default="")
    cnpj = models.CharField(max_length=11, null=True, blank=True, default="")
    responsavel = models.OneToOneField(Pessoa, on_delete=models.CASCADE)
    inscricao_estadual = models.CharField(max_length=50, null=True, blank=True, default="")
    inscricao_municipal = models.CharField(max_length=50, null=True, blank=True, default="")
    logo = models.ImageField(upload_to='empresa_logos/%Y/%m/%d/', null=True, blank=True)

    def logo_preview(self):
        from django.utils.html import escape
        if (self.logo):
            return mark_safe(u'<img src="%s" width="64" height="64"/>' % escape(self.logo.url))
        else:
            return mark_safe('<img src="" />')
    logo.short_description = 'Foto Preview'
    logo.allow_tags = True
    
    email = models.EmailField(null=True, blank=True, default="")
    website = models.URLField(null=True, blank=True, default="")
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    fones = models.ManyToManyField(Fone, through="PessoaJuridica_Fones")
    observacao = models.CharField(max_length=400, null=True, blank=True, default="")
    ativo = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    oper = models.IntegerField(default=0)
    tenant_system = models.ForeignKey(TenantSystem, on_delete=models.PROTECT)


"""     def __str__(self):
        return f"{self.id}|{self.razao_social}|{self.cnpj}|{self.responsavel.nome}\
        |{self.responsavel.data_nascimento}|{self.responsavel.cpf}|\
        {self.responsavel.identidade}|{self.ativo}"
 """


class Colaborador(models.Model):
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE)
    observacao = models.CharField(max_length=255, null=True)
    ativo = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    oper = models.IntegerField(default=0)
    tenant_system = models.ForeignKey(TenantSystem, on_delete=models.PROTECT)


"""     def __str__(self):
        return f"{self.id}|{self.pessoa.nome}|{self.pessoa.data_nascimento}|{self.pessoa.cpf}|\
        {self.pessoa.identidade}|{self.ativo}"
 """


class Cliente(models.Model):
    pessoa_fisica = models.ForeignKey(
        Pessoa, on_delete=models.SET_NULL, null=True)
    pessoa_juridica = models.ForeignKey(
        PessoaJuridica, on_delete=models.SET_NULL, null=True)

    EMPROSPECCAO = 'P'
    EMCONTRATO = 'E'
    CPFOUCNPJNAOAPROVADO = 'N'
    CPFOUCNPJAPROVADO = 'A'

    TIPOCLIENTE_OPCOES = [
        (EMPROSPECCAO, 'Prospecção - Possível Cliente'),
        (CPFOUCNPJAPROVADO, 'Aprovado - CPF/CNPJ'),
        (CPFOUCNPJNAOAPROVADO, 'Não Aprovado - CPF/CNPJ'),
        (EMCONTRATO, 'Em contrato')
    ]

    tipo_cliente = models.CharField(
        max_length=1, choices=TIPOCLIENTE_OPCOES, default=EMPROSPECCAO)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    observacao = models.CharField(max_length=255, null=True)
    ativo = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    oper = models.IntegerField(default=0)
    tenant_system = models.ForeignKey(TenantSystem, on_delete=models.PROTECT)


"""     def __str__(self):
        if self.pessoa_fisica is not None:
            return f"{self.id}|{self.pessoa_fisica.cpf}|{self.pessoa_fisica.nome}|{self.pessoa_fisica.data_nascimento}|\
            {self.pessoa_fisica.identidade}|{self.ativo}"
        elif self.pessoa_juridica is not None:
            return f"{self.id}|{self.pessoa_juridica.cnpj}|{self.pessoa_juridica.razao_social}|{self.ativo}"
        else:
            return None
 """


class PessoaJuridica_Fones(models.Model):
    client_pessoa_juridica = models.ForeignKey(
        PessoaJuridica, on_delete=models.CASCADE)
    fone = models.ForeignKey(Fone, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    oper = models.IntegerField(default=0)
    tenant_system = models.ForeignKey(TenantSystem, on_delete=models.PROTECT)


class PessoaFisica_Fones(models.Model):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    fone = models.ForeignKey(Fone, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    oper = models.IntegerField(default=0)
    tenant_system = models.ForeignKey(TenantSystem, on_delete=models.PROTECT)


class SimulacaoCpfCnpj(models.Model):
    client = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_simulacao = models.DateField(auto_now_add=True)
    score_serasa = models.IntegerField()
    risco_serasa = models.IntegerField()
    aprovado = models.BooleanField(default=False)
    ativo = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    oper = models.IntegerField(default=0)
    tenant_system = models.ForeignKey(TenantSystem, on_delete=models.PROTECT)


class SimulacaoFinanceiraCustosOperacionais(models.Model):
    client = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_simulacao = models.DateField(auto_now_add=True)
    valor_requisitado_imovel = models.DecimalField(
        max_digits=15, decimal_places=2)
    numero_requisitado_meses = models.IntegerField()

    ITAU = 'I'
    SANTANDER = 'S'
    CAIXA = 'C'
    BRADESCO = 'B'
    OUTROS = 'O'
    BANCO_OPCOES = [
        (ITAU, 'Banco ITAU'),
        (SANTANDER, 'Banco SANTANDER'),
        (CAIXA, 'CAIXA ECONOMICA FEDERAL'),
        (BRADESCO, 'BRADESCO'),
        (OUTROS, 'OUTROS')
    ]

    banco = models.CharField(
        max_length=1, choices=BANCO_OPCOES, default=SANTANDER)
    porcentagem_entrada = models.DecimalField(max_digits=15, decimal_places=2)
    valor_imovel = models.DecimalField(max_digits=15, decimal_places=2)
    valor_entrada = models.DecimalField(max_digits=15, decimal_places=2)
    valor_financiado = models.DecimalField(max_digits=15, decimal_places=2)
    simulacao_aprovada_pelo_cliente = models.BooleanField(default=False)
    ativo = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    oper = models.IntegerField(default=0)
    tenant_system = models.ForeignKey(TenantSystem, on_delete=models.PROTECT)


class ContratoImobiliario(models.Model):
    client = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    quantia_liquida = models.DecimalField(max_digits=15, decimal_places=2)
    valor_pagar_ato_assinatura = models.DecimalField(
        max_digits=15, decimal_places=2)
    valor_pagar_agent_aprovacao_credito = models.DecimalField(
        max_digits=15, decimal_places=2)
    data_contrato = models.DateField()
    testemunha1 = models.CharField(max_length=100, blank=True)
    testemunha1_cpf = models.CharField(max_length=11, null=False)
    testemunha2 = models.CharField(max_length=100, blank=True)
    testemunha2_cpf = models.CharField(max_length=11, null=False)
    esta_pago_valor_assinatura = models.BooleanField(default=False)
    esta_pago_valor_agente_aprovacao_credito = models.BooleanField(
        default=False)
    esta_assinado = models.BooleanField(default=False)
    ativo = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    oper = models.IntegerField(default=0)
    tenant_system = models.ForeignKey(TenantSystem, on_delete=models.PROTECT)


class ArquivosCliente(models.Model):
    client = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    contrato = models.ForeignKey(
        ContratoImobiliario, on_delete=models.SET_NULL, null=True)
    nome_arquivo = models.CharField(max_length=255, null=False)
    descricao_arquivo = models.CharField(max_length=255, null=False)
    tamanho_arquivo_bytes = models.IntegerField()

    WORD = 'W'
    EXCEL = 'E'
    CSV = 'C'
    TXT = 'T'
    PDF = 'P'
    IMG = 'I'
    VIDEO = 'V'
    OUTROS = 'O'

    TIPOARQUIVO_OPCOES = [
        (WORD, 'Documento do Microsoft Word'),
        (EXCEL, 'Planilha do Microsoft Excel'),
        (CSV, 'Arquivo .CSV'),
        (TXT, 'Arquivo de Texto Puro'),
        (PDF, 'Arquivo PDF'),
        (IMG, 'Arquivo de Imagem'),
        (VIDEO, 'Arquivo de Vídeo'),
        (OUTROS, 'Tipo de Arquivo não Informado')
    ]

    tipo_arquivo = models.CharField(
        max_length=1, choices=TIPOARQUIVO_OPCOES, default=PDF)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    oper = models.IntegerField(default=0)
    tenant_system = models.ForeignKey(TenantSystem, on_delete=models.PROTECT)
 """