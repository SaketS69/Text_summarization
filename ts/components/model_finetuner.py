import pytorch_lightning as pl
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM 
import torch
from ts.exceptions import CustomException
import sys
from ts.constants import LEARNING_RATE


class T5smallFinetuner(pl.LightningModule):
    try: 
        def __init__(self, model, tokenizer):
            super().__init__()
            self.model = model
            self.tokenizer = tokenizer
        
        def forward(self, input_ids, attention_mask,
                    decoder_attention_mask=None, labels=None):
            
            outputs = self.model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                decoder_attention_mask=decoder_attention_mask,
                labels=labels
            )
            return outputs.loss
        
        def _step(self, batch):
            source_input_ids, source_attention_mask, target_input_ids, target_attention_mask = batch
            
            loss = self(
                input_ids=source_input_ids,
                attention_mask=source_attention_mask,
                decoder_attention_mask=target_attention_mask,
                labels=target_input_ids
            )
            return loss
            
        def training_step(self, batch, batch_idx):
            loss = self._step(batch)
            self.log("train_loss", loss, prog_bar=True, logger=True)  # Log training loss
            return loss
        
        def validation_step(self, batch, batch_idx):
            loss = self._step(batch)
            self.log("val_loss", loss, prog_bar=True, logger=True)  # Log validation loss
            return loss
        
        # Use hooks instead of deprecated methods
        def on_train_epoch_end(self):
            # Optionally, handle any actions at the end of training epoch
            pass
        
        def on_validation_epoch_end(self):
            # Optionally, handle any actions at the end of validation epoch
            pass

        def configure_optimizers(self):
            optimizer = torch.optim.AdamW(self.model.parameters(), lr=LEARNING_RATE)
            scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=3)
            return {
                'optimizer': optimizer,
                'lr_scheduler': scheduler,
                'monitor': 'val_loss'
            }
        
    except Exception as e:
        raise CustomException(e, sys)
