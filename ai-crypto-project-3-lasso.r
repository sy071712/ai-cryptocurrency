library('stringr')
library('glmnet')

# 함수 정의
extract <- function(o, s) { 
  index <- which(coef(o, s) != 0) 
  data.frame(name = rownames(coef(o))[index], coef = coef(o, s)[index]) 
}

options(scipen = 999)

# 파일 이름 설정
filtered <- "2024-05-01T000000-2024-05-01T235900-upbit-BTC-filtered-5-2-mid5.csv"
model_file <- "2024-05-01T235900-upbit-BTC-lasso-5s-2std.csv"

# 데이터 로드 및 전처리
if (file.exists(filtered)) {  # 파일이 존재하는지 확인
  filtered <- read.csv(filtered)
  mid_std <- sd(filtered$mid_price)
  message(round(mid_std, 0))

  filtered_no_time_mid <- subset(filtered, select = -c(mid_price, timestamp))

  y <- filtered_no_time_mid$return
  x <- subset(filtered_no_time_mid, select = -c(return))

  x <- as.matrix(x)

  # Lasso 회귀 모델 학습
  cv_fit <- cv.glmnet(x = x, y = y, alpha = 1, intercept = FALSE, lower.limits = 0, nfolds = 5) # lasso

  fit <- glmnet(x = x, y = y, alpha = 1, lambda = cv_fit$lambda.1se, intercept = FALSE, lower.limits = 0)

  # 모델 계수 추출 및 저장
  df <- extract(fit, s = cv_fit$lambda.1se)
  df <- t(df)
  write.table(df, file = model_file, sep = ",", col.names = FALSE, row.names = FALSE, quote = FALSE)
}
