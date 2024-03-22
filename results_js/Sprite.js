class Sprite extends Phaser.GameObjects.Container{
	constructor(){
		super(window.main)
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

	swapChildren(ch1, ch2){
		this.swap(ch1, ch2)
	}

	addChild(spr){
		this.add(spr);
		this.bringToTop(spr);
	}

	removeFromParent(dispose=false){
		if (this.parentContainer){
			this.parentContainer.remove(this)
		}
		this.removeFromDisplayList()
	}

	removeChild(spr){
		if (spr.parentContainer==this){
			this.remove(spr)
		}
	}

	getChildIndex(spr){
		this.getIndex(spr);
	}

	addChildAt(spr, id){
		this.addAt(spr, id);
	}
	getChildAt(id){
		return this.getAt(id)
	}
	getBounds(out){
		return super.getBounds(out)
	}
	getVisibleBounds(output){
        if (output === undefined) { output = new Phaser.Geom.Rectangle(); }

        output.setTo(this.x, this.y, 0, 0);

        if (this.parentContainer)
        {
            var parentMatrix = this.parentContainer.getBoundsTransformMatrix();
            var transformedPosition = parentMatrix.transformPoint(this.x, this.y);

            output.setTo(transformedPosition.x, transformedPosition.y, 0, 0);
        }

        if (this.list.length > 0)
        {
            var children = this.list;
            var tempRect = new Phaser.Geom.Rectangle();
            var hasSetFirst = false;

            

            for (var i = 0; i < children.length; i++)
            {
                var entry = children[i];

                if (entry.getBounds)
                {
					if (entry.visible){
						if (entry.getVisibleBounds){
							entry.getVisibleBounds(tempRect)
						}else{
							entry.getBounds(tempRect);
						}
						

						if (!hasSetFirst)
						{
							output.setEmpty();
							output.setTo(tempRect.x, tempRect.y, tempRect.width, tempRect.height);
							hasSetFirst = true;
						}
						else
						{
							Phaser.Geom.Rectangle.Union(tempRect, output, output);
						}					
					}

                }
            }
        }

        return output;
	}
	getTouchableBounds(output){
        if (output === undefined) { output = new Phaser.Geom.Rectangle(); }

        output.setTo(this.x, this.y, 0, 0);

        if (this.parentContainer)
        {
            var parentMatrix = this.parentContainer.getBoundsTransformMatrix();
            var transformedPosition = parentMatrix.transformPoint(this.x, this.y);

            output.setTo(transformedPosition.x, transformedPosition.y, 0, 0);
        }

        if (this.list.length > 0)
        {
            var children = this.list;
            var tempRect = new Phaser.Geom.Rectangle();
            var hasSetFirst = false;

            for (var i = 0; i < children.length; i++)
            {
                var entry = children[i];

                if (entry.getBounds)
                {
					if (entry.visible && entry.touchable){
						if (entry.getTouchableBounds){
							entry.getTouchableBounds(tempRect);
						}else{
							entry.getBounds(tempRect);
						}
						

						if (!hasSetFirst)
						{
							output.setEmpty();
							output.setTo(tempRect.x, tempRect.y, tempRect.width, tempRect.height);
							hasSetFirst = true;
						}
						else
						{
							Phaser.Geom.Rectangle.Union(tempRect, output, output);
						}					
					}

                }
            }
        }

        return output;
	}
	getBoundsOfChild(output, child){
        if (output === undefined) { output = new Phaser.Geom.Rectangle(); }

        output.setTo(this.x, this.y, 0, 0);

        if (this.parentContainer)
        {
            var parentMatrix = this.parentContainer.getBoundsTransformMatrix();
            var transformedPosition = parentMatrix.transformPoint(this.x, this.y);

            output.setTo(transformedPosition.x, transformedPosition.y, 0, 0);
        }

        if (this.list.length > 0)
        {
            var children = this.list;
            var tempRect = new Phaser.Geom.Rectangle();
            var hasSetFirst = false;

            for (var i = 0; i < children.length; i++)
            {
                var entry = children[i];

                if (entry.getBounds)
                {
					if (entry==child){
						if (entry.getTouchableBounds){
							entry.getTouchableBounds(tempRect);
						}else{
							entry.getBounds(tempRect);
						}
						

						if (!hasSetFirst)
						{
							output.setEmpty();
							output.setTo(tempRect.x, tempRect.y, tempRect.width, tempRect.height);
							hasSetFirst = true;
						}
						else
						{
							Phaser.Geom.Rectangle.Union(tempRect, output, output);
						}					
					}

                }
            }
        }

        return output;
	}

	getLocalVisibleBounds(){
		var rct = this.getVisibleBounds(new Phaser.Geom.Rectangle());
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

	getLocalTouchableBounds(){
		var rct = this.getTouchableBounds(new Phaser.Geom.Rectangle());
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
	getLocalBoundsOfChild(child){
		var rct = this.getBoundsOfChild(new Phaser.Geom.Rectangle(), child);
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

	get parent(){
		return this.parentContainer
	}

	get numChildren(){
		return this.length
	}
}