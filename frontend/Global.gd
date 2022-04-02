extends Node


# Declare member variables here. Examples:
# var a = 2
# var b = "text"

var token = null
var username = null

var HOST_NAME = "localhost"
var PORT_NAME = "8000"
var SCHEME = "http"
var URL_BASE = SCHEME + "://" + HOST_NAME + ":" + PORT_NAME + "/api/"
var HOME_PAGE = "."

var FILEBROWSER_SCENE_PATH = "res://filebrowser.tscn"


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
