from django.db import models
#Un lexers permite dividir la fuente en tokens, fragmentos de la fuente que tienen un tipo de token determinando que texto reppresenta semanticamente. Al igual que en un IDE se diferencias las palabras clave como "class, method, def, etc".
from pygments.lexers import get_all_lexers
#Son estilos para "remarcar" 
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

# Create your models here.

LEXERS = [item for item in get_all_lexers() if item [1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item,item) for item in get_all_styles()])


#Un snippet es una "porcion" o fraccion de codigo reutilizable. Tambien puede ser codigo maquina o texto.
class Snippet(models.Model):

    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly' , max_length=100)

    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args,**kwargs)

    class Meta:
        ordering = ['created']

