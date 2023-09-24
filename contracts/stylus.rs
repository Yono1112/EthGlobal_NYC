// stylus.rs
use ethers::contract::{Contract, EthCall, EthDisplay};
use ethers::prelude::*;

#[derive(Clone, EthCall, EthDisplay)]
#[ethcall(name = "HelloScroll")]
struct HelloScroll {
    message: String,

    #[ethcall(name = "updateMessage", abi = "updateMessage(string)")]
    update_message: fn(new_message: String) -> Result<(), EthCallError>,
}

struct MessageHistory {
   messages: Vec<String> 
}

impl MessageHistory {

  fn add_message(&mut self, message: String) {
    self.messages.push(message);
  }

  fn get_messages(&self) -> Vec<String> {
    self.messages.to_vec() 
  }

}

// Stylusコントラクト
#[ethers::contract]
pub struct Stylus {
  hello_scroll: HelloScroll,
  history: MessageHistory 
}

impl Stylus {

  pub fn new(hello_scroll_address: Address) -> Self {
    let hello_scroll = HelloScroll::new(hello_scroll_address);
    let history = MessageHistory { messages: vec![] };

    Self {
      hello_scroll,
      history 
    }
  }

  pub fn update_and_save(&mut self, new_message: String) -> Result<(), EthCallError> {
    self.hello_scroll.update_message(new_message)?;

    let message = self.hello_scroll.message().unwrap();
    self.history.add_message(message);

    Ok(())
  }

}