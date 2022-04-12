const express= require('express');

const router = express.Router();
const Post = require('../models/Post');
const { body, validationResult } = require('express-validator');

router.get('/', async (req,res)=>{
    try{
        const posts = await Post.find().sort({ _id: -1 });
        res.json(posts);
    }catch (err){
        res.json({message : err});
    }
});

router.get('/:pitchID', async (req,res)=>{

    Post.find({_id : req.params.pitchID }, function(err, result)
    {
        //console.log(err);
    console.log("result");
    console.log(result);
    //console.log(result.length)
    if(result!=null && result.length!=0 )
    {

        res.status(201);
       // console.log("Reached");
       res.json(result);
        
        //res.send(req.params.postID);
    }
    else{
        res.status(404);
       // console.log("Bello");
        res.json({message : "Pitch Not Found"});
        res.status(404);
    }
    }
    )



    
});


router.post('/',(req,res) => {
    //console.log(req.body);

   
    try { 
        res.status(201);
        const post = new Post({
         

            entrepreneur:req.body.entrepreneur,
        
            pitchTitle:req.body.pitchTitle,
        
            pitchIdea:req.body.pitchIdea,
        
            askAmount:req.body.askAmount,
        
            equity: req.body.equity,
        });
        
        post.save();
        res.json(post._id);
       
      // console.log(res.status);
        
      } catch (error) {
        // something here
        res.status(400);
      }
    
});



router.post('/:postID/makeOffer',(req,res) =>{
// console.log(req.params.postID);
// console.log(req.body);

var offered={
            
    "investor":req.body.investor,

"amount": req.body.amount,

"equity": req.body.equity,

"comment":req.body.comment

};
// const offer = new Post();


Post.find({_id : req.params.postID }, function(err, result)
{
    console.log(err);
    console.log("result");
    console.log(result);
    if(result!=null && result.length !=0 )
    {
        res.status(201);
        console.log("Reached");
        
        Post.findOneAndUpdate(
            { _id: req.params.postID }, 
            { $push: { offers: offered  } },
            function (error, success) {
                    if (error==null || sucess==null) {
                        console.log("error");
                        console.log(error);
                    } else {
                        console.log("Success");
                        console.log(success);
                    }
                });
        res.send(req.params.postID);
    }
    else{
        res.status(404);
        console.log("Bello");
        res.json({message : "Pitch Not Found"});
        res.status(404);
    }
})

// Post.findOneAndUpdate(
//     { _id: req.params.postID }, 
//     { $push: { offers: offered  } },
//     function (error, success) {
//             if (error) {
//                 console.log(error);
//             } else {
//                 console.log(success);
//             }
//         });
// res.send(req.params.postID);



 

}
);
module.exports =router;