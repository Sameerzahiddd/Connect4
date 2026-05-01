⏺ Here's what the research says and what I recommend for our      
  specific case:                                                
                                                                  
  Two techniques are relevant:                                    
                                                            
  1. Structured output prompting — define the exact JSON schema,  
  show one perfect example, strict formatting rules. Gets 99%+    
  schema compliance. Essential for our use case since Lindy parses
   the output directly into sheet columns.                        

  2. Chain of Thought (CoT) — make the LLM reason step by step    
  before answering. Improves accuracy 15-40% on tasks where
  multiple criteria interact. Adds tokens/cost but worth it for   
  complex classification.

  Our classification is complex enough to warrant both. It needs  
  to simultaneously assess change type, customer impact, two
  boolean flags, AND write a coherent summary. That's 5           
  interdependent decisions from unstructured input. CoT will catch
   edge cases that a flat prompt misses — like a bug fix that's
  also a breaking change, or a feature that's behind a flag.

  My recommendation — hybrid approach:                            
  
  Add a reasoning field to the JSON output where the LLM thinks   
  out loud first, then fills in the actual fields based on that
  reasoning. Lindy can ignore the reasoning field when writing to 
  the sheet but it makes the output debuggable.

  {
    "reasoning": "This PR adds a new login flow... it affects end 
  users directly... Sales should know...",                        
    "change_type": "new_feature",
    "customer_impact": "customer_facing",                         
    "summary": "...",
    "include_sales": "yes",                                       
    "include_cs": "no"
  }                                                               
                  
  Also want to add one concrete few-shot example in the prompt — a
   real input/output pair. That alone dramatically reduces
  misclassification.                                              
                  
  Want to go ahead and implement this in the prompt file?         
  
  Sources:                                                        
  - Structured Output Prompting Guide
  - Chain-of-Thought Prompting Guide 2026  