suppressPackageStartupMessages({
  library(readr); library(dplyr); library(tidyr); library(forcats)
})

DATA_DIR <- file.path("src","data")
TRAIN <- file.path(DATA_DIR,"train.csv")
TEST  <- file.path(DATA_DIR,"test.csv")
OUT   <- file.path(DATA_DIR,"predictions_r.csv")

message("[INFO] Loading: ", TRAIN)
train <- read_csv(TRAIN, show_col_types = FALSE)
message("[OK] Train rows=", nrow(train), " cols=", ncol(train))
message("[INFO] Columns: ", paste(names(train), collapse=", "))

prep <- function(df){
  df %>% mutate(
    Sex      = as.factor(Sex),
    Embarked = fct_explicit_na(as.factor(Embarked), "Unknown"),
    Age  = ifelse(is.na(Age), median(Age, na.rm=TRUE), Age),
    Fare = ifelse(is.na(Fare), median(Fare, na.rm=TRUE), Fare)
  )
}

train2 <- prep(train)
formula <- Survived ~ Pclass + Sex + Age + SibSp + Parch + Fare + Embarked
model <- glm(formula, data=train2, family=binomial())
message("[OK] Model trained.")
print(coef(summary(model)))

# quick train accuracy (mirrors step 16 style)
p_tr <- predict(model, type="response")
yhat <- ifelse(p_tr>=0.5,1L,0L)
acc  <- mean(yhat==train2$Survived, na.rm=TRUE)
message(sprintf("[METRIC] Train accuracy = %.3f", acc))

# predict on test
message("[INFO] Loading: ", TEST)
test <- read_csv(TEST, show_col_types = FALSE)
test2 <- prep(test)
p_te <- predict(model, newdata=test2, type="response")
pred <- ifelse(p_te>=0.5,1L,0L)

write_csv(tibble(PassengerId=test$PassengerId, Survived_pred=pred), OUT)
message("[OK] Saved predictions to: ", OUT)
