from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from ..extensions.database import mongo
from bson.objectid import ObjectId

produto = Blueprint('produto', __name__)

@produto.route('/list')
def listProdutos():
    if "username" in session:
        produtos = mongo.db.produtos.find()
        return render_template("produtos/list.html", produtos=produtos)
    else:
        return redirect(url_for("usuario.index"))

@produto.route('/insert', methods=["GET", "POST"])
def insertProduto():
    if request.method == "GET":
        return render_template("produtos/insert.html")
    else:
        nome = request.form.get('nome')
        estoque = request.form.get('estoque')  
        quantidade = request.form.get('quantidade')
        preco = request.form.get('preco')
        categoria = request.form.get('categoria')  

        if not nome:
            flash("Campo 'nome' é obrigatório")  
        elif not estoque:
            flash("Campo 'estoque' é obrigatório.") 
        elif not quantidade:
            flash("Campo 'quantidade' é obrigatório.")
        elif not categoria:
            flash("Campo 'categoria' é obrigatório.")
        elif not preco:
            flash("Campo 'preco' é obrigatório.")
        else:
            mongo.db.produtos.insert_one(
                {
                    "produto": nome,
                    "estoque": estoque,
                    "categoria": categoria,
                    "quantidade": quantidade,
                    "preco": preco,
                    "valor_total": (float(quantidade) * float(preco))     
                }
            )
            flash('Produto criado com sucesso!')
        return redirect(url_for("produto.listProdutos"))

@produto.route('/edit', methods=["GET", "POST"])
def editProduto():
    if request.method == "GET":
       idproduto = request.values.get("idproduto")
       
       if not idproduto:
          flash("Campo 'idproduto' é obrigatório.")
          return redirect(url_for("produto.listProduto"))
       else:
           idprod = mongo.db.produtos.find({"_id": ObjectId(idproduto)})
           produto = [prd for prd in idprod]
           estoques = set()
           produtos = mongo.db.produtos.find()
           for p in produtos:
               estoques.add(p["estoque"])
           return render_template(
               "produtos/edit.html", produto=produto, estoques=estoques
           )
    else:
        idproduto = request.form.get("idproduto")
        nome = request.form.get("nome")
        estoque = request.form.get("estoque")
        categoria = request.form.get("categoria")
        preco = request.form.get("preco")
        quantidade = request.form.get("quantidade")
        categorias = ["Informática", "Papelaria"]

    if not idproduto:
        flash("Campo 'idproduto' é obrigatório.")

    elif not nome:
         flash("Campo 'nome' é obrigatório.")

    elif not estoque:
         flash("Campo 'estoque' é obrigatorio ")

    elif not quantidade:
         flash("Campo 'quantidade' é obrigatório.")

    elif not categoria:
         flash("Campo 'categoria' é obrigatório.")

    elif not preco:
         flash("Campo 'preco' é obrigatorio ")

    else:
        mongo.db.produtos.update_one({"_id": ObjectId(idproduto)},
        {
             "$set": {
                     "produto": nome,
                     "estoque": estoque,
                     "quantidade": quantidade,
                     "preco": preco,
                     "categoria": categoria,
                     "valor_total": (float(quantidade) * float(preco))
             }
        })
        flash("Produto alterado com sucesso!")
    return redirect(url_for("produto.listProdutos"))    
        

@produto.route('/delete')
def deleteProduto():
    idproduto = request.values.get("idproduto")
    if not idproduto:
        flash("Campo 'idproduto' é obrigatório")
    else:
        mongo.db.produtos.delete_one({"_id": ObjectId(idproduto)})
        flash("Produto deletado com sucesso!")
    return redirect(url_for("produto.listProdutos"))