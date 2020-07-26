var House = collie.Class({
	$init : function () {
    this.set({class_name : "House"});
    this._initObject();
  },

  _initObject : function () {
    // this._oText = new collie.Text({
		// 	x : 120,
		// 	y : -50,
		// 	textAlign : "center",
		// 	fontSize : 35,
    //   fontWeight:"",
		// 	width : 200,
		// 	height : 30,
		// 	fontColor : "#707070"
		// }).addTo(this).text("Lv." + this.get("level") + " (" + this.get("qt") + "/" + this.get("capacity") + "\)");
  },

}, collie.DisplayObject);
