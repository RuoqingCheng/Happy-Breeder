var Cat = collie.Class({
	$init : function () {
    this.set({class_name : "Cat"});
    this._initObject();
  },

  _initObject : function () {
		var text  = "$ " + parseInt(this.get("price")) + " age:" + parseInt(this.get("age"));
		this._oText = new collie.Text({
			x : 65,
			y : 390,
			fontSize : 40,
			width : 250,
			height : 30,
			fontColor : "#FFA500"
		}).addTo(this).text(text);

    this._bar_health = new SkillBar({
			y : -20,
		})
    this._bar_health.blank();
    this._bar_health.addTo(this);

    this._bar_clean = new SkillBar({
			y : -50,
		})
    this._bar_clean.blank();
    this._bar_clean.addTo(this);

    this._bar_food = new SkillBar({
			y : -80,
		})
    this._bar_food.blank();
    this._bar_food.addTo(this);

		this._fur_amount = new SkillBar({
			y : -110,
		})
    this._fur_amount.blank();
    this._fur_amount.addTo(this);

		this.mate = new collie.DisplayObject({
			x: 0,
      y: 370,
      scaleX: 0.7,
      scaleY: 0.7,
      scale : 0.7,
      useEvent: true,
      backgroundImage: "mate",
			visible: false,
    }).addTo(this)

  },

	ready_to_mate: function() {
		this.mate.set("visible", true);
	},

	not_ready_to_mate: function() {
		this.mate.set("visible", false);
	},

	update_price_age : function (price, age) {
    this._oText.text("$" + parseFloat(parseInt(price)) + " age:" + parseFloat(parseInt(age)));
  },

	update_fur_amount: function(a) {
		this.set({fur_amount : a})
		this._fur_amount.percent(this.get("fur_amount"));
	},

	update_cleaness: function(a) {
		this.set({level_clean : a})
		this._bar_clean.percent(this.get("level_clean"));
	},

	update_health: function(a) {
		this.set({level_health : a})
		this._bar_health.percent(this.get("level_health"));
	},

	update_food: function(a) {
		this.set({level_food : a})
		this._bar_food.percent(this.get("level_food"));
	},

  show_skill_bar : function () {
    this._bar_health.addtext("Health");
    this._bar_health.setcolor("#FFE26D");
    this._bar_health.percent(this.get("level_health"));

    this._bar_clean.addtext("Cleaness");
    this._bar_clean.setcolor("#5CC7FF");
    this._bar_clean.percent(this.get("level_clean"));

    this._bar_food.addtext("Food");
    this._bar_food.setcolor("#99E897");
    this._bar_food.percent(this.get("level_food"));

		this._fur_amount.addtext("Furball");
    this._fur_amount.setcolor("#ff9999");
    this._fur_amount.percent(this.get("fur_amount"));
  },

  hide_skill_bar : function () {
    this._bar_clean.blank();
    this._bar_food.blank();
    this._bar_health.blank();
		this._fur_amount.blank();
  },

}, collie.DisplayObject);
