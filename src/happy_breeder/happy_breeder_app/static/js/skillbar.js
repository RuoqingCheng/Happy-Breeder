var SkillBar = collie.Class({
	$init : function () {
		this.set({
			backgroundColor : "rgba(255,255,255, 0.8)",
      x : 55,
			width : 220,
			height : 19,
		});
		this._initObject();
	},

	_initObject : function () {
		this._oGauge = new collie.DisplayObject({
			x : 0,
			y : 2,
			width : 0,
			height : 15,
			defaultColor: "yellow",
			backgroundColor : "yellow"
		}).addTo(this);

    this._oText = new collie.Text({
			x : -150,
			y : 0,
			textAlign : "right",
			fontSize : 30,
			width : 140,
			height : 30,
			fontColor : "#707070"
		}).addTo(this).text("");
	},

  addtext : function (t) {
    this._oText.text(t);
  },

  setcolor : function (c) {
    this.set("backgroundColor", "rgba(255,255,255, 0.5)");
    this._oGauge.set("backgroundColor", c);
		this._oGauge.set("defaultColor", c);
  },

  blank : function () {
    this.set("backgroundColor", "");
    this._oGauge.set("backgroundColor", "");
    this._oText.text("");
  },

	percent : function (nPercent) {
		if (isNaN(nPercent) || nPercent < 0) {
			nPercent = 0;
		}

		if (nPercent > 1) {
			nPercent = 1;
		}

		this._oGauge.set("width", Math.round(this.get("width") * nPercent));

		if (nPercent <= 0.2) {
			this._oGauge.set("backgroundColor", "red");
		} else {
			this._oGauge.set("backgroundColor", this._oGauge.get("defaultColor"));
		}
	}
}, collie.DisplayObject);
