img_path = "../static/imgs/"

collie.ImageManager.add({
  oreo: img_path + "oreo_nobgr.png",
  cereal: img_path + "cereal_nobgr.png",
  house: img_path + "house.png"
});

var layer = new collie.Layer({
  width: 500,
  height: 200,
});

movable_obj = null;
htStartPosition = {};
htSelectedDisplayObjectPosition = {};
oLayer = null;
var oLayer = new collie.Layer({
  width: 900,
  height: 400,
});

collie.util.addEventListener(window, "load", function () {
  oConsole = new collie.FPSConsole({color: "rgba(0, 0, 0, 0)",}); //hide
  var htParams = collie.util.queryString();
  var nCount = htParams.count ? htParams.count : 100;
  var htSize = {
    width: document.body.clientWidth,
    height: document.body.clientHeight
  };


  collie.Renderer.DEBUG_RENDERING_MODE = typeof htParams.dom != "undefined" ? "dom" : (typeof htParams.canvas !=
    "undefined" ? "canvas" : "auto");



  mousedown_fn = function (oEvent) {
    if (oEvent.displayObject) {
      if (oEvent.displayObject.get("class_name") == "Cat" || oEvent.displayObject.get("class_name") == "House" ) {
        movable_obj = oEvent.displayObject;
        movable_obj.set({
          scaleX: oEvent.displayObject.get("scale") * 1.1,
          scaleY: oEvent.displayObject.get("scale") * 1.1
        });

        htStartPosition = {
          x: oEvent.x,
          y: oEvent.y
        };
        htSelectedDisplayObjectPosition = {
          x: movable_obj.get("x"),
          y: movable_obj.get("y")
        };
      }
    }
    // movable_obj.show_skill_bar();
  },

  mouseup_fn = function (oEvent) {
    if (movable_obj !== null) {
      oEvent.displayObject.set({
        scaleX: oEvent.displayObject.get("scale"),
        scaleY: oEvent.displayObject.get("scale")
      });

      movable_obj = null;
      htSelectedDisplayObjectPosition = htStartPosition = {};

      oLayer.removeChild(oEvent.displayObject);
      oLayer.addChild(oEvent.displayObject);
    }
  },

  mousemove_fn = function (oEvent) {
    if (movable_obj !== null) {
      var x = htStartPosition.x - oEvent.x;
      var y = htStartPosition.y - oEvent.y;
      movable_obj.set({
        x: htSelectedDisplayObjectPosition.x - x,
        y: htSelectedDisplayObjectPosition.y - y
      });
    }
  }

  var oSelectedDisplayObject = null;
  var htStartPosition = {};
  var htSelectedDisplayObjectPosition = {};

  var cat_cereal = new Cat({
    x: 400,
    y: 20,
    scaleX: 0.3,
    scaleY: 0.3,
    scale : 0.3,
    useEvent: true,
    backgroundImage: "cereal",
    level_health: 0.2,
    level_clean: 0.5,
    level_food: 0.6,
    id: "1"
  }).addTo(oLayer).show_skill_bar();

  var house = new House({
    x: -100,
    y: -50,
    scaleX: 0.4,
    scaleY: 0.4,
    scale : 0.4,
    useEvent: true,
    backgroundImage: "house",
    level: 1,
    qt: 2,
    capacity: 5,
  }).addTo(oLayer)

  oLayer.attach({
    mousedown: mousedown_fn,
    mouseup:mouseup_fn,
    mousemove:mousemove_fn,
  });

  oConsole.load();
  collie.Renderer.addLayer(oLayer);
  collie.Renderer.load(document.getElementById("cat"));
  collie.Renderer.start("30fps");
});

{% for c in cats %}
var cat = new Cat({
  x: 300,
  y: 100,
  scaleX: 0.3,
  scaleY: 0.3,
  scale : 0.3,
  useEvent: true,
  backgroundImage: "oreo",
  level_health: {{c.health}}/100,
  level_clean: {{c.cleanness}}/100,
  level_food: {{c.food_level}}/100,
  id: {{c.id}}
}).addTo(oLayer).show_skill_bar();

{% endfor %}
