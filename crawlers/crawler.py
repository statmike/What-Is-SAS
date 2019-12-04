# imports
import crawlers.actions_by_product.actions_by_product as crawl_actions
import crawlers.viya_procs.viya_procs as crawl_viya_procs
import crawlers.procs_by_product.procs_by_product as crawl_procs

# crawl action sets and actions
actions_by_product_url='https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.5&docsetId=allprodsactions&docsetTarget=actionSetsByProduct.htm&locale=en'
products = crawl_actions.products(actions_by_product_url,'Yes')
action_sets = crawl_actions.action_sets(products,'Yes')
actions = crawl_actions.actions(action_sets,'Yes')

# crawl all procedures
procs_by_product_url='https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.5&docsetId=allprodsproc&docsetTarget=p1vzipzy6l8so0n1gbbh3ae63czb.htm&locale=en'
procs = crawl_procs.procs(procs_by_product_url,'Yes')
procs_plus = crawl_procs.procs_plus(procs,'Yes')
procs_linked = crawl_procs.procs_linked(procs_plus,'Yes')

# crawl viya procedures
viya_procs_url='https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.5&docsetId=allprodsproc&docsetTarget=p1o1v16by0iotvn10m0jzzv9i3y8.htm&locale=en#'
viya_procs = crawl_viya_procs.procs(viya_procs_url,'Yes')


#list(products)
#list(action_sets)
#list(actions)
#list(procs)
#list(procs_plus)
#list(procs_linked)
#list(viya_procs)
