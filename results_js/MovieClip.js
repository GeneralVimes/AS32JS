class MovieClip extends StarlingImage{
	constructor(txAr){
		super(txAr?txAr[0]:null)
		this.framesAr=txAr.slice()
		this.frameId=0;
	}

	get currentFrame(){
		return this.frameId
	}

	get numFrames(){
		return this.framesAr.length
	}

	set currentFrame(val){
		if (val<0){
			val=0;
		}
		this.frameId=val%this.framesAr.length;
		this.startlingTexture = this.framesAr[this.frameId]
	}
}