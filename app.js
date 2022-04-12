const express = require('express');

var app = express();

var mongoose=require("mongoose");
var bodyParser=require('body-parser');

app.use(bodyParser.json());
var dbURL=require("./properties").DB_URL;
mongoose.connect(dbURL);

const postsRoute = require('./routes/pitch');
app.use('/pitches', postsRoute);

mongoose.connection.on("connected",()=>{
    console.log("connected to mongo ");
});

app.listen(8081);