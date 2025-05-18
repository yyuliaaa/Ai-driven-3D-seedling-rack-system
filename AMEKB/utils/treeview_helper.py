def expand_treeview(treeview):
    for item in treeview.get_children():
        treeview.item(item, open=True)
        for child in treeview.get_children(item):
            treeview.item(child, open=True)