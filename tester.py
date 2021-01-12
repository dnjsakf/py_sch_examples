from typing import Optional, Union, Any, Callable

class BaseField(object):
  def __init__(
      self,
      valtype:Any=None,
      required:Optional[bool]=False,
      default_value:Union[Callable,str]=None,
      **kwargs
    ):
    self.value = None
    self.type = valtype
    self.required = required
    self.options = dict(kwargs)
  
  # 값 설정
  def setValue(self, value):
    # 값이 있는 경우 타입체크
    if value is not None and not isinstance(value, self.type):
      raise TypeError("Expacted data type '%s', but '%s'." %( self.type.__name__, value.__class__.__name__ ))
    
    # 유효성검사
    self.validate(value)
    
    self.value = value
    
  def getValue(self):
    return self.value
    
  def getOption(self, optkey, defaultvalue):
    return self.options.get(optkey, defaultvalue)
  
  # Override
  def validate(self, value=None):
    pass
  
  def __str__(self):
    return str(self.value)

# 문자열 필드
class StringField(BaseField):
  def __init__(self, maxlength:Optional[int]=None, **kwargs):
    super(StringField, self).__init__(str)
    
    # 유효성검사 옵션값
    self.maxlength = maxlength
  
  # Override: 유효성검사
  def validate(self, value=None):
    value = value or self.getValue()
    exists = value is not None
    
    # 유효성검사: 필수값
    if bool(self.required) and not exists:
      raise ValueError("Value is None")
    
    # 유효성검사: 최대길이
    if bool(self.maxlength) and exists and len(value) > self.maxlength:
      raise ValueError("Expacted value length %d, but %d." % ( self.maxlength, len(value) ))

  
text = StringField(required=True, maxlength=10)
text.setValue("")

print( text )