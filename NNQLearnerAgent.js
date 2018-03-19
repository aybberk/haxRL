class NNQLearnerAgent extends Agent {
    constructor() {
        super();
        this.experienceReplay = new ExperienceReplay(10000);
        let stateDim = 4;
        let hiddenSize = 200;
        this.brain = new NeuralNetwork(stateDim, hiddenSize, 9).setLoss("mse");
        this.targetbrain = new NeuralNetwork(stateDim, hiddenSize, 9).setLoss("mse");
        this.targetbrain.copyWeightsFrom(this.brain);

        this.discount = 0.999;
        this.sars = {};
        this.actionRepeat = 5;
        this.targetUpdateFreq = 10;
        this.epsilon = 0.1;

        this.repeatCooldown = 0;
        this.targetUpdateCooldown = 0;
        this.lastAction = null;

    }


    act() {
        if (this.repeatCooldown > 0) { //repeat action
            this.repeatCooldown--;
            this.player.applyAction(this.lastAction);
        } else { //select new action
            this.repeatCooldown = this.actionRepeat;
            this.sars.s = this.getStateInfo();

            let actionIndex;
            if (Math.random() < this.epsilon) {
                actionIndex = Math.floor(Math.random() * 9);
            } else {
                actionIndex = this.brain.predict(this.sars.s);
            }
            let action = Object.values(Action)[actionIndex];
            this.sars.a = actionIndex;
            this.player.applyAction(action);
            this.lastAction = action;
        }
    }

    getStateInfo() {
        return ([
            this.ball.center.x,
            this.ball.center.y,
            this.player.center.x,
            this.player.center.y,
        ]);
    }

    getReward(s, a, ss) {
        let sBallPos = new Vector(s[0], s[1]);
        let sPlayerPos = new Vector(s[2], s[3]);

        let ssBallPos = new Vector(ss[0], ss[1]);
        let ssPlayerPos = new Vector(ss[2], ss[3]);

        let sDist = Vector.dist(sPlayerPos, sBallPos);
        let ssDist = Vector.dist(ssPlayerPos, ssBallPos);

        let ballVelocity = -Vector.sub(ssBallPos, sBallPos).x;
        let ballToLeft = ballVelocity > 0.5;
        let closing = ssDist < sDist - 0.5;
        let close = ssDist < 100;
        let reward = close ? 1 : -1;
        console.log(reward);

        return reward;


    }

    learn() {
        if (this.repeatCooldown == 0) { //means new action to be made
            this.sars.ss = this.getStateInfo();
            this.sars.r = this.getReward(this.sars.s, this.sars.a, this.sars.ss);
            this.experienceReplay.addExperience(this.sars);
            let batchSize = 1; //for now
            let expBatch = this.experienceReplay.sampleExperience(batchSize);

            for (let n = 0; n < batchSize; n++) {

                let {
                    s,
                    a,
                    r,
                    ss
                } = expBatch[n];

                let y = r + this.discount * this.targetbrain.predict(ss, true);

                if (this.env.state.episodeEnd) {
                    y = r;
                }

                let target = this.brain.forward(s).dataSync();
                target[a] = y;
                this.brain.trainStep(s, target);
            }

            if (this.targetUpdateCooldown == 0) {
                this.targetbrain.copyWeightsFrom(this.brain);
                this.targetUpdateCooldown = this.targetUpdateFreq;
            } else {
                this.targetUpdateCooldown--;
            }
        }
    }
}