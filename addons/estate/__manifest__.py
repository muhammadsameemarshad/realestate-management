{
    'name':"Real-Estate Management",
    'version':'14.1.0',
    'depends':['base'],
    'sequence':'1',
    'author':"Sameem Arshad",
    'category':'Category',
    'description':"""This is a  module of Real-Estate Management for Axiom World""",
    'data': [
    'security/ir.model.access.csv',
    'views/estate_menu.xml',
    'views/estate_property_views.xml',
    'views/estate_property_type.xml',
    'views/estate_property_tag.xml',
    'views/estate_property_offer.xml',
    'views/user_inherited.xml',


],

    'installable': True,
    'auto_install': False,
    'application':  True,
}