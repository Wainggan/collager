

import justpy as jp

css = """

body div {
	display: flex;
	background: blue;
	height: 100vh;
}

.sidebar {
	width: max(16rem, 20%);
}

.sidebar-uploadButton {
	padding: 0.2rem;
	background: #888;
	border: #666 1px solid;
}


"""

def build_table(size):
	table = jp.Table()

	for y in range(size[1]):
		row = jp.Tr(a= table)

		for x in range(size[0]):
			cell = jp.Td(a= row)
			cell.style = "background: #eee; border: #999 1px solid"
			jp.P(text= f"x {x} y {y}", a= cell)
	
	return table

def build_sidebar():
	sidebar = jp.Div()
	sidebar.classes = "sidebar bg-red"

	uploadButton = jp.Button(text= "upload!!", a= sidebar)
	uploadButton.classes = "sidebar-uploadButton"

	return sidebar


def serve():
	wp = jp.WebPage()
	wp.css = css

	sidebar = build_sidebar()
	wp.add(sidebar)

	

	content = jp.Div(a= wp)
	content.classes = "content"

	table = build_table((4, 4))
	table.classes = "grid"
	content.add(table)

	return wp

jp.justpy(serve)
