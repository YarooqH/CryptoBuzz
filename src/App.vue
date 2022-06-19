<template>
  <b-container class="mb-5">
    <b-row class="header-row">
      <b-col>
        <h1>CryptoBuzz</h1>
        <p>Buy and Create your Buzz Light-years.</p>
      </b-col>
    </b-row>

    <b-row>
      <b-col class="action-container text-center">
        <h4>Buy a random Buzz</h4>
        <img :src="unknownBuzzImg" class="unknown-Buzz">
        <b-button type="button" v-on:click="buyBuzz()">Buy</b-button>
        <p>Each Buzz costs 0.02 Ether</p>
      </b-col>
      <b-col cols="2" class="middle-container">
        <h3 v-if="!isLoading">or</h3>
      </b-col>
      <b-col class="action-container">
        <h4>Create two of the Buzzes you own to make a new one!</h4>
        <b-form>
          <b-form-group id="based"
                        label="Based ID:"
                        label-for="based">
            <b-form-input id="based"
                          v-model="based"
                          required
                          placeholder="Enter Based ID">
            </b-form-input>
          </b-form-group>
          <b-form-group id="suit"
                        label="Suit ID:"
                        label-for="suit">
            <b-form-input id="suit"
                          v-model="suit"
                          required
                          placeholder="Enter Suit ID">
            </b-form-input>
          </b-form-group>
          <b-button v-on:click="createBuzzes" type="button">Create Buzzes</b-button>
          <p>Createing Buzzes cost 0.05 Ether</p>
        </b-form>
      </b-col>
    </b-row>

    <hr>
    <h2 class="mb-5">Owned Buzzes</h2>

    <b-row v-if="Buzzes.length == 0">
      <b-col>
        <h2>No Buzzes owned yet!</h2>
      </b-col>
    </b-row>

    <b-row v-for="i in Math.ceil(Buzzes.length / 3)" v-bind:key="i">
      <b-col cols="4" v-for="item in Buzzes.slice((i - 1) * 3, i * 3)"
             v-bind:item="item"
             v-bind:key="item.id">
        <b-card style="height:400px;" class="mb-2">
          <b-img thumbnail fluid :src="item.url" class="image"/>
          <p class="card-text mt-2 text-center">
            <b>ID:</b> {{ item.id }}
            <br>
            <b>Origin:</b>
            <span v-if="item.based == 0 && item.suit == 0">Bought</span>
            <span v-else>{{ item.based }} & {{ item.suit }}</span>
          </p>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import getWeb3 from '../contracts/web3';
import contractAbi from '../contracts/abi';
import Buzz1 from './assets/Buzz/1.png';
import Buzz2 from './assets/Buzz/2.png';
import Buzz3 from './assets/Buzz/3.png';
import Buzz4 from './assets/Buzz/4.png';
import Buzz5 from './assets/Buzz/5.png';
import Buzz6 from './assets/Buzz/6.png';
import BuzzX from './assets/Buzz/unknown.png';

const contractAddress = '0xd9145CCE52D386f254917e481eB44e9943F39138'; 
const BuzzesMap = [null, Buzz1, Buzz2, Buzz3, Buzz4, Buzz5, Buzz6];

export default {
  name: 'App',
  data() {
    return {
      web3: null,
      account: null,
      contractInstance: null,
      gene: null,
      based: null,
      suit: null,
      unknownBuzzImg: BuzzX,
      Buzzes: [],
      isLoading: false,
    };
  },
  mounted() {
    getWeb3().then((res) => {
      this.web3 = res;
      this.contractInstance = new this.web3.eth.Contract(contractAbi, contractAddress);
      this.web3.eth.getAccounts().then((accounts) => {
        [this.account] = accounts;
        this.getBuzzes();
      }).catch((err) => {
        console.log(err, 'err!!');
      });
    });
  },
  methods: {
    buyBuzz() {
      this.isLoading = true;
      this.contractInstance.methods.buyBuzz().send({
        from: this.account,
        value: web3.toWei(0.02, 'ether'),
      }).then((receipt) => {
        this.addBuzzFromReceipt(receipt);
        this.isLoading = false;
      }).catch((err) => {
        console.log(err, 'err');
        this.isLoading = false;
      });
    },
    createBuzzes() {
      this.isLoading = true;
      this.contractInstance.methods.createBuzzes(this.based, this.suit).send({
        from: this.account,
        value: web3.toWei(0.05, 'ether'),
      }).then((receipt) => {
        this.addBuzzFromReceipt(receipt);
        this.isLoading = false;
      }).catch((err) => {
        console.log(err, 'err');
        this.isLoading = false;
      });
    },
    getBuzzes() {
      this.isLoading = true;
      this.contractInstance.methods.ownedBuzzes().call({
        from: this.account,
      }).then((receipt) => {
        for (let i = 0; i < receipt.length; i += 1) {
          this.contractInstance.methods.getBuzzDetails(receipt[i]).call({
            from: this.account,
          }).then((Buzz) => {
            this.Buzzes.push({
              id: Buzz[0],
              genes: Buzz[1],
              based: Buzz[2],
              suit: Buzz[3],
              url: BuzzesMap[Buzz[1]],
            });
          }).catch((err) => {
            console.log(err, 'err');
          });
        }
        this.isLoading = false;
      }).catch((err) => {
        console.log(err, 'err');
        this.isLoading = false;
      });
    },
    addBuzzFromReceipt(receipt) {
      // Utility function to add a newly created Buzz to our list
      this.Buzzes.push({
        id: receipt.events.Birth.returnValues.BuzzId,
        genes: receipt.events.Birth.returnValues.genes,
        based: receipt.events.Birth.returnValues.basedId,
        suit: receipt.events.Birth.returnValues.suitId,
        url: BuzzesMap[receipt.events.Birth.returnValues.genes],
      });
    },
  },
};
</script>

<style lang="css">
@import url('https://fonts.googleapis.com/css?family=Poppins:400,500');

* {
  font-family: 'Poppins', sans-serif;
}
button {
  width: 100%;
}
.header-row {
  text-align: center;
  margin: 30px 0;
}
.action-container h4 {
  text-align: center;
  margin-bottom: 30px;
}
.action-container p {
  text-align: center;
  margin-top: 10px;
}
.middle-container {
  display: flex;
  justify-content: center;
  align-items: center;
}
.middle-container img {
  height: 100px;
}
.unknown-Buzz {
  height: 180px;
  width: 180px;
  margin: 9px 0;
}
</style>
