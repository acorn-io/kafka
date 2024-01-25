FROM ruby:3.3.0

WORKDIR /app

COPY Gemfile Gemfile.lock ./

RUN gem install bundler
RUN bundle install

COPY . .

CMD ["ruby", "producer.rb"]
