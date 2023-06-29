def test_cart_page_objects(app):

    app.open()

    app.add_popular_items_to_cart(3)

    app.clear_cart()
