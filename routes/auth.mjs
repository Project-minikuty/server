import express from "express";
import db from "../db/connection.mjs";
import { ObjectId } from "mongodb";

const router = express.Router();
router.get("/",(req,res)=>{
    res.send("<h1>hello world in auth</h1>")
});

router.get("/validate",async (req,res)=>{
     let users = db.collection("users");
     users.findOne({name :req.query.username},{projection:{_id:0}},(err,result)=>{
        if(err){
            res.status(500).json({message:"server error try again"})
        }else if(result){
            if(result.password==req.query.password){
                res.status(200).json({message:"success",
            type:result.type})
            }else{
            res.status(401).json({message:"password wrong"});}
        }else{
            res.status(404).json({message:"user not found"});
        }
     });
     
});

router.post("/create",(req,res)=>{
    let users = db.collection("users");
    let id = ObjectId();
    let newUser = {_id:id,
        name:req.query.username,
        password:req.query.password,
        type:req.query.type};
        users.findOne({name :req.query.username},{projection:{_id:0}},(err,result)=>{
            if(err){
                res.status(500).json({message:"server error try again",err:err})
            }else if(result){
                
                res.status(401).json({message:"user already exists"});
            }else{
                users.insertOne(newUser,(err,result)=>{
                    if(err){
                        res.status(500).json({message:"server error try again",err:err});
                    }
                    else if(result.acknowledged){
                        res.status(200).json({message:"user created",result:result});
                    }else{
                        res.status(201).json({message:"usernot created",result:result});
                    }
                });
            }
         });
    
});

export default router;