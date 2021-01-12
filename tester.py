from typing import Optional, Union, Any, Callable, Iterable

class BaseField(object):
  def __init__(
      self,
      valtype:Any,
      name:str=None,
      required:Optional[bool]=False,
      default_value:Union[Callable,str]=None,
      **kwargs
    ):
    self.value = None
    self.type = valtype
    self.name = name
    self.required = required
    self.options = dict(kwargs)
  
  # 값 설정
  def setValue(self, value:Any, validate:Optional[bool]=True):
    if validate:
      # 값이 있는 경우 타입체크
      if value is not None and not isinstance(value, self.type):
        raise TypeError("Expacted data type '%s', but '%s'." %( self.type.__name__, value.__class__.__name__ ))
      
      # 유효성검사
      self.validate(value)
    
    self.value = value

  def getType(self):
    return self.type
    
  def getValue(self):
    return self.value
    
  def getOption(self, optkey, defaultvalue=None):
    return self.options.get(optkey, defaultvalue)
  
  # Override
  def validate(self, value=None):
    pass
  
  def __str__(self):
    return str(self.value)

# 문자열 필드
class StringField(BaseField):
  def __init__(self, maxlength:Optional[int]=None, **kwargs):
    super(StringField, self).__init__(str, **kwargs)
    
    # 유효성검사 옵션값
    self.maxlength = maxlength
  
  # Override: 유효성검사
  def validate(self, value=None):
    value = value or self.getValue()
    exists = value is not None
    
    # 유효성검사: 필수값
    if bool(self.required) and not exists:
      raise ValueError("This value was Required, but it is None.")
    
    # 유효성검사: 최대길이
    if bool(self.maxlength) and exists and len(value) > self.maxlength:
      raise ValueError("Expacted value length %d, but %d." % ( self.maxlength, len(value) ))

class BaseModel(object):
  def __init__(self, data:Optional[Union[dict,Iterable]]=None, **kwargs):
    pass

  def getFields(self):
    fields = list()
    for field_name in dir(self):
      field_class = getattr(self, field_name)
      if not callable(field_class) and not field_name.startswith("_"):
        if isinstance(field_class, BaseField):
          fields.append((field_name, field_class))
    return fields

  # 값만 매핑
  def dump(self, data:dict):
    for field_name, field_class in self.getFields():
      value = data.get(field_name, None) or data.get(field_class.name, None)
      field_class.setValue(value, validate=False)
    return dict([(field_name, field_class.getValue()) for field_name, field_class in self.getFields()])

  # 값을 매핑하면서 유효성검사까지
  def load(self, data:dict):
    for field_name, field_class in self.getFields():
      value = data.get(field_name, None) or data.get(field_class.name, None)
      field_class.setValue(value)
    return dict([(field_class.name or field_name, field_class.getValue()) for field_name, field_class in self.getFields()])

  def __str__(self):
    return str(self.getFields())

class DummyModel(BaseModel):
  id = StringField(name="ID", required=True, maxlength=10)
  name = StringField(name="NAME", maxlength=10)

text1 = StringField(required=True, maxlength=10)
text1.setValue("text1")

text2 = StringField(required=True, maxlength=10)
text2.setValue("text2")

model1 = DummyModel()
model1_data = model1.dump({
  "name": "model1"
})
model2 = DummyModel()

print( text1 )
print( text2 )

print( model1_data )
print( model2 )
