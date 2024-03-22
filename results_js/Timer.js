class Timer{
	constructor(delay=1000, repeatCount=0){
		this.onTimerTick=null;
		this.onTimerComplete=null;

		this.currentTimesTicked = 0;
		this.neededTimesTicked = repeatCount;
		this.msBetweenTicks = delay;

		this.ticker = null;
	}
	/**
	 * The total number of times the timer has fired since it started
	 * at zero. If the timer has been reset, only the fires since
	 * the reset are counted.
	 * @langversion	3.0
	 * @playerversion	Flash 9
	 * @playerversion	Lite 4
	 */
	get currentCount (){
		return this.currentTimesTicked
	}
	/**
	 * The delay, in milliseconds, between timer
	 * events. If you set the delay interval while
	 * the timer is running, the timer will restart
	 * at the same repeatCount iteration.
	 * Note: A delay lower than 20 milliseconds is not recommended. Timer frequency
	 * is limited to 60 frames per second, meaning a delay lower than 16.6 milliseconds causes runtime problems.
	 * @langversion	3.0
	 * @playerversion	Flash 9
	 * @playerversion	Lite 4
	 * @throws	Error Throws an exception if the delay specified is negative or not a finite number.
	 */
	get delay () {
		return this.msBetweenTicks
	}
	set delay (val){
		this.msBetweenTicks = val;
		if (this.ticker){
			clearInterval(this.ticker)
			setInterval(this.onTimer.bind(this),this.msBetweenTicks)
		}
	}
	/**
	 * The total number of times the timer is set to run.
	 * If the repeat count is set to 0, the timer continues forever 
	 * or until the stop() method is invoked or the program stops.
	 * If the repeat count is nonzero, the timer runs the specified number of times. 
	 * If repeatCount is set to a total that is the same or less then currentCount
	 * the timer stops and will not fire again.
	 * @langversion	3.0
	 * @playerversion	Flash 9
	 * @playerversion	Lite 4
	 */
	get repeatCount () {
		return this.neededTimesTicked
	}
	set repeatCount (val){
		this.neededTimesTicked=val;
		if (this.neededTimesTicked<=this.currentTimesTicked){
			this.stop()
		}
	}
	/**
	 * The timer's current state; true if the timer is running, otherwise false.
	 * @langversion	3.0
	 * @playerversion	Flash 9
	 * @playerversion	Lite 4
	 */
	get running () {
		return this.ticker!=null
	}
	/**
	 * Stops the timer, if it is running, and sets the currentCount property back to 0,
	 * like the reset button of a stopwatch. Then, when start() is called,
	 * the timer instance runs for the specified number of repetitions,
	 * as set by the repeatCount value.
	 * @langversion	3.0
	 * @playerversion	Flash 9
	 * @playerversion	Lite 4
	 */
	reset () {
		this.stop();
		this.currentTimesTicked=0;
	}
	
	addEventListener(type, listener){
		if (type=="timer"){
			this.onTimerTick=listener
		}
		if (type=="timerComplete"){
			this.onTimerComplete=listener
		}
	}

	hasEventListener(type){
		var res=false;
		if (type=="timer"){
			res = this.onTimerTick!=null
		}
		if (type=="timerComplete"){
			res = this.onTimerComplete!=null
		}
		return res;
	}

	removeEventListener(type, listener){
		if (type=="timer"){
			this.onTimerTick=null
		}
		if (type=="timerComplete"){
			this.onTimerComplete=null
		}
	}	
	/**
	 * Starts the timer, if it is not already running.
	 * @langversion	3.0
	 * @playerversion	Flash 9
	 * @playerversion	Lite 4
	 */
	start () {
		if (!this.ticker){
			this.ticker = setInterval(this.onTimer.bind(this),this.msBetweenTicks);
		}
	}
	/**
	 * Stops the timer. When start() is called after stop(), the timer
	 * instance runs for the remaining number of repetitions, as set by the repeatCount property.
	 * @langversion	3.0
	 * @playerversion	Flash 9
	 * @playerversion	Lite 4
	 */
	stop () {
		if (this.ticker){
			clearInterval(this.ticker)
			this.ticker=null
		}
	}

	onTimer(){
		this.currentTimesTicked+=1;
		if (this.onTimerTick){
			this.onTimerTick();
		}
		if (this.currentTimesTicked==this.neededTimesTicked){
			this.stop()
			if (this.onTimerComplete){
				this.onTimerComplete();
			}
			
		}
	}
}