const express = require('express');

var app = express();

var mongoose=require("mongoose");
var bodyParser=require('body-parser');
// const url='mongodb://localhost:27017/xharktank'
// mongoose.connect(url,{useNewUrlParser :true})
// const conn=mongoose.connection
// conn.on('open', () =>{
//     console.log("connected to mongo ");
// })
app.use(bodyParser.json());
var dbURL=require("./properties").DB_URL;
mongoose.connect(dbURL);

const postsRoute = require('./routes/pitch');
app.use('/pitches', postsRoute);
app.get('/', (req,res)=>{
res.send("hello");
})
mongoose.connection.on("connected",()=>{
    console.log("connected to mongo ");
});
//app.set('port', 8081);
// var listener = app.listen(8081);
//     console.log('Listening on port ' + listener.address().port); //Listening on port 8888

app.listen(8081,() =>{
    console.log("server is running...")
});
