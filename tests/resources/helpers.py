import openpay


class MyResource(openpay.resource.APIResource):
    pass


class MySingleton(openpay.resource.SingletonAPIResource):
    pass


class MyListable(openpay.resource.ListableAPIResource):
    pass


class MyCreatable(openpay.resource.CreateableAPIResource):
    pass


class MyUpdateable(openpay.resource.UpdateableAPIResource):
    pass


class MyDeletable(openpay.resource.DeletableAPIResource):
    pass


class MyComposite(openpay.resource.ListableAPIResource,
                  openpay.resource.CreateableAPIResource,
                  openpay.resource.UpdateableAPIResource,
                  openpay.resource.DeletableAPIResource):
    pass
