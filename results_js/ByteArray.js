class ByteArray{
	static defineLenFromArray(ar){//each array item is written as Double (8 bytes)
		return ar.length*8+8//first ar length ir written and then the contents
	}
	static defineLenFromHexString(str){//each 2 letters represent 1 byte
		return str.length/2
	}
	static defineLenFromBase64String(str){//each 4 symbols represent 3 bytes
		var remLen = str.length % 4;
		var res = 3*Math.floor(str.length/4)
		if (remLen==3){
			res+=2
		}
		if (remLen==2){
			res+=1
		}
		return res
	}
	constructor(lenInBytes){
		if (!lenInBytes){
			throw(new Error("Define the length of ByteArray when creatoing it"))
		}
		this.lenInBytes=lenInBytes
		this.position=0

		this.buffer=new ArrayBuffer(this.lenInBytes)
		this.view = new DataView(this.buffer)
	}

	get bytesAvailable(){
		return this.lenInBytes-this.position
	}

	writeDouble(val){
		this.view.setFloat64(this.position, val)
		this.position+=8
	}

	readDouble(){
		let res = this.view.getFloat64(this.position)
		this.position+=8
		return res;
	}
	writeByte(val){
		this.view.setInt8(this.position,val)
		this.position+=1
	}
	readByte(){
		let res = this.view.getInt8(this.position)
		this.position+=1
		return res;
	}
	readUnsignedInt(){

	}
	toString(){
	
	}
	readUTFBytes(len){
	
	}
	compress(){
		var compressedAr = pako.deflate(new Uint8Array(this.buffer))
		// console.log(compressedAr)
		this.buffer=compressedAr.buffer
		this.view = new DataView(this.buffer)
		this.lenInBytes=compressedAr.byteLength
		this.position=0		
	}
	uncompress(){
		var unCompressedAr = pako.inflate(new Uint8Array(this.buffer))
		// console.log(unCompressedAr)
		this.buffer=unCompressedAr.buffer
		this.view = new DataView(this.buffer)
		this.lenInBytes=unCompressedAr.byteLength
		this.position=0		
	}
}