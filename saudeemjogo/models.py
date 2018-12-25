from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import CASCADE


class TiposModulo(models.Model):
    """
		Tipos de módulos
	"""
    nome = models.CharField(max_length=80)

    class Meta:
        verbose_name = 'Tipos de Módulo'
        verbose_name_plural = 'Tipos de Módulos'

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        self.nome = self.nome.title()
        super().save(*args, **kwargs)


class Medico(models.Model):
    perfil = models.IntegerField(null=True, blank=False)
    salario = models.IntegerField(null=True, blank=False)
    expertise = models.CharField(max_length=1)
    atendimento = models.CharField(max_length=1)
    pontualidade = models.CharField(max_length=1)

    def save(self, *args, **kwargs):
        if not self.expertise.isalpha():
            raise ValueError("Expertise deve ser uma letra entre A e Z")
        if not self.atendimento.isalpha():
            raise ValueError("Atendimento deve ser uma letra entre A e Z")
        if not self.pontualidade.isalpha():
            raise ValueError("Pontualidade deve ser uma letra entre A e Z")
        self.expertise = self.expertise.upper()
        self.pontualidade = self.pontualidade.upper()
        self.atendimento = self.atendimento.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return "Médico perfil: " + str(self.perfil)


class Modulo(models.Model):
    """
		Módulos comprados pelos hospitais
	"""
    nome = models.ForeignKey(TiposModulo, on_delete=CASCADE)
    custo_aquisicao = models.IntegerField(null=True, blank=False)
    custo_por_mes = models.IntegerField(null=True, blank=False)
    tecnologia = models.CharField(max_length=1)
    conforto = models.CharField(max_length=1)
    capacidade = models.IntegerField(null=True, blank=False)
    preco_do_tratamento = models.IntegerField(null=True, blank=False)

    def save(self, *args, **kwargs):
        if not self.tecnologia.isalpha():
            raise ValueError("Tecnologia deve ser uma letra entre A e Z")
        if not self.conforto.isalpha():
            raise ValueError("Conforto deve ser uma letra entre A e Z")
        self.conforto = self.conforto.upper()
        self.tecnologia = self.conforto.upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'

    def __str__(self):
        return str(self.nome) + " " + str(self.id)


class MedicoModulo(models.Model):
    medico = models.ForeignKey(Medico, on_delete=CASCADE)
    modulo = models.ForeignKey(Modulo, on_delete=CASCADE)

    class Meta:
        verbose_name = 'Médico no módulo'
        verbose_name_plural = 'Médicos nos módulos'

    def __str__(self):
        return str(self.medico) + " em " + str(self.modulo)


class Hospital(models.Model):
    """
		Hospital organizado pelos jogadores
		Os jogadores alterarão diretamente os hospitais
	"""
    nome = models.CharField(max_length=80, primary_key=True)
    caixa = models.IntegerField(null=True, blank=False, default=25000)
    emprestimos = models.IntegerField(null=True, blank=True)
    modulos = models.ManyToManyField(Modulo,blank=True)
    medicos = models.ManyToManyField(Medico,blank=True)
    medicos_modulos = models.ManyToManyField(MedicoModulo, blank=True)

    def save(self, *args, **kwargs):
        if self.caixa < 0:
            raise ValueError("Valor de caixa menor que 0")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Hospital'
        verbose_name_plural = 'Hospitais'

    def __str__(self):
        return self.nome

    def atribuir_medico_ao_modulo(self, medico, modulo):
        try:
            me = self.medicos.filter(id=medico)[0]
        except ObjectDoesNotExist:
            raise ValueError("Médico:" + str(medico) + " não existe")
        try:
            mo = self.modulos.filter(id=modulo)[0]
        except ObjectDoesNotExist:
            raise ValueError("Módulo:" + str(modulo) + " não existe")
        mm = MedicoModulo(medico=me, modulo=mo)
        mm.save()
        self.medicos_modulos.add(mm)

    def comprar_modulo(self, modulo):
        try:
            m = Modulo.objects.get(id=modulo)
            valor = m.custo_aquisicao
            if self.realizar_pagamento(valor):
                self.modulos.add(m)
                return True
            else:
                return False
        except ObjectDoesNotExist:
            raise NameError("Módulo com o nome" + str(modulo) + " não existe")
        except TypeError:
            raise TypeError("tipo inválido.")
        except Exception as e:
            return str(e)

    def realizar_pagamento(self, valor):
        if self.caixa - valor >= 0:
            self.caixa = self.caixa - valor
            return True
        return False
