extends Node2D


# Declare member variables here. Examples:
# var a = 2
# var b = "text"

onready var Header = $MarginContainer/VBoxContainer/header
onready var nav = $MarginContainer/VBoxContainer/navigation
onready var nav_edit = nav.get_node("path")
onready var nav_edit_button = nav.get_node("commit_path")
onready var items_container = $MarginContainer/VBoxContainer/ScrollContainer/VBoxContainer

var pathnow = ""

# Called when the node enters the scene tree for the first time.
func _ready():
	$HTTPRequest.connect("request_completed", self, "on_request_complete")
	nav_edit_button.connect("pressed", self, "on_nav_commited")
	
	get_dir(Global.HOME_PAGE)
	_on_viewport_size_changed()
	get_tree().get_root().connect("size_changed", self, "_on_viewport_size_changed")

func _on_viewport_size_changed():
	$MarginContainer.rect_size = get_viewport().size
	$MarginContainer.rect_min_size = get_viewport().size
	var scroll_pos = $MarginContainer/VBoxContainer/ScrollContainer.rect_position
	$MarginContainer/VBoxContainer/ScrollContainer.rect_size =  Vector2(get_viewport().size.x - 40, get_viewport().size.y - scroll_pos.y - 40)
	$MarginContainer/VBoxContainer/ScrollContainer.rect_min_size =  Vector2(get_viewport().size.x - 40, get_viewport().size.y - scroll_pos.y - 40)


func get_dir(dirname):
	nav_edit.editable = false
	nav_edit_button.disabled = true
	$HTTPRequest.request(Global.URL_BASE + "files/ls/", ["token: " + Global.token], false, HTTPClient.METHOD_POST, JSON.print({"filepath": dirname}))

func on_request_complete(result, response_code, headers, body):
	while true:
		var body_parse_result = JSON.parse(body.get_string_from_utf8())
		if body_parse_result.error:
			popup_info({"detail": "can't parse received json"})
			return
		
		var body_json = body_parse_result.result
		
		if (response_code != 200):
			popup_info(body_json)
			return
		for n in items_container.get_children():
			items_container.remove_child(n)
			n.queue_free()
		
		for item in body_json:
			var l = Label.new()
			l.text = item
			items_container.add_child(l)
		
		pathnow = nav_edit.text
		break
		
	nav_edit.editable = true
	nav_edit_button.disabled = false
	
func on_nav_commited():
	get_dir("./" + nav_edit.text)

func popup_info(detail):
	$Popup/CenterContainer/VBoxContainer/Label.text = detail["detail"]
	$Popup.visible = true
	$Popup/CenterContainer/VBoxContainer/Button.connect("pressed", self, "on_popup_confirm")

func on_popup_confirm():
	$Popup.visible = false
	nav_edit.editable = true
	nav_edit_button.disabled = false
