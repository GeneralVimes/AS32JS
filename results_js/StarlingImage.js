class StarlingImage extends Phaser.GameObjects.Image{
	constructor(tx){
		super(window.main,0,0,tx?tx.atlas:"ALL_ART", tx?tx.frame:"w000_FontEur4nemo0000")
		this.scene = window.main
        this.touchable = true;
        this.touchGroup = false;
        // this.x",
        // this.y",
        // this.rotation",
        // this.scale",
        // this.scaleX",
        // this.scaleY",
        // this.alpha",
        // this.visible",
        // this.parent"		
	}

	removeFromParent(spr){
		if (this.parentContainer){
			this.parentContainer.remove(this)
		}
		this.removeFromDisplayList()
	}

	getBounds(out){
		return super.getBounds(out)
	}

	getLocalBounds(){
		var rct = this.getBounds(new Phaser.Geom.Rectangle());
		let x0 = rct.left
		let y0 = rct.top
		let x1 = rct.right
		let y1 = rct.bottom
		let pt0 = this.getLocalPoint(x0, y0)
		let pt1 = this.getLocalPoint(x1, y1)
		rct.left = Math.min(pt0.x, pt1.x)
		rct.right = Math.max(pt0.x, pt1.x)
		rct.top = Math.min(pt0.y, pt1.y)
		rct.bottom = Math.max(pt0.y, pt1.y)	
		return rct
	}	
	// вот так сатвить нельзя, т.к. конфликтует с сеттером имеджа
	//надо будет смотреть по коду
	// set texture(tx){
	// 	super.setTexture(tx.atlas, tx.frame)
	// }
	
	/**
	 * @param {{ atlas: string; frame: string | number; }} val
	 */
	set startlingTexture(val){
		if (val){
			super.setTexture(val.atlas, val.frame)
		}
	}

	alignPivot(horz, vert){
		if ((horz!=null)&&(horz!=undefined)){
			if ((vert!=null)&&(vert!=undefined)){
				var xp=0.5;
				var yp=0.5;
				if (horz=="center"){
					xp=0.5
				}else{
					if (horz=="left"){
						xp=0
					}else{
						if (horz=="right"){
							xp=1;
						}else{
							xp=horz
						}
					}
				}
				if (vert=="center"){
					yp=0.5
				}else{
					if (vert=="top"){
						yp=0
					}else{
						if (vert=="bottom"){
							yp=1;
						}else{
							yp=vert
						}
					}
				}
				this.setOrigin(xp, yp)
			}
		}
	}
	readjustSize(){
	
	}

	get parent(){
		return this.parentContainer
	}

	set color(val){
		this.tint=val
	}	

	get color(){
		return this.tint
	}
}