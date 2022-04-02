extends Node2D


# Declare member variables here. Examples:
# var a = 2
# var b = "text"

onready var ui_container = $CenterContainer/VBoxContainer
onready var username_edit = ui_container.get_node("HBoxContainer/username")
onready var password_edit = ui_container.get_node("HBoxContainer2/password")
onready var login_button = ui_container.get_node("Button")
onready var errormessage = ui_container.get_node("errormssage")

# Called when the node enters the scene tree for the first time.
func _ready():
	login_button.connect("pressed", self, "on_login_pressed")
	$HTTPRequest.connect("request_completed", self, "on_login_request_complete")
	_on_viewport_size_changed()
	get_tree().get_root().connect("size_changed", self, "_on_viewport_size_changed")

func _on_viewport_size_changed():
	$CenterContainer.rect_size = get_viewport().size
	$CenterContainer.rect_min_size = get_viewport().size

func on_login_pressed():
	errormessage.visible = false
	login_button.disabled = true
	
	var username = username_edit.text
	if username.empty():
		errormessage.text = "username shouldn't be empty"
		errormessage.visible = true
		login_button.disabled = false
		return
	var password = password_edit.text
	if password.empty():
		errormessage.text = "password shouldn't be empty"
		errormessage.visible = true
		login_button.disabled = false
		return
	
	Global.username = username
	$HTTPRequest.request(Global.URL_BASE + "login", PoolStringArray(), false, HTTPClient.METHOD_POST, JSON.print({"name": username, "password": password}))

func on_login_request_complete(result, response_code, headers, body):
	while true:
		if response_code != 200:
			errormessage.text = String(response_code)
			break
		
		var body_parse_result = JSON.parse(body.get_string_from_ascii())
		if body_parse_result.error != OK:
			errormessage.text = "server error: can't parse the result as json"
			break
		
		var body_json = body_parse_result.result
		if not body_json["ok"]:
			errormessage.text = body_json["message"]
			password_edit.text = ""
			break
		errormessage.text = ""
		Global.token = body_json["token"]
		
		get_tree().change_scene(Global.FILEBROWSER_SCENE_PATH)
		return
		
	login_button.disabled = false
	errormessage.visible = true
	Global.username = null
